# --- Streamlit Cloud sqlite3 workaround -------------------------------------
# Chroma needs a newer sqlite3 than Streamlit Cloud ships. If pysqlite3-binary
# is installed (add it to requirements.txt), swap it in. Locally this is a no-op.
# This MUST run before `import chromadb`.
try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from pypdf import PdfReader
import hashlib
import io
import os
import re
import json
import zipfile
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="United Brands — Relevant Market Chatbot", page_icon="🍌")

CASE_NAME = "United Brands v Commission (Case 27/76)"
CHUNKS_FOLDER = "Chunks - United Brands v Commission - Relevant Product Market"

# The upload & chunk tool is only needed when creating the chunk files. Once
# they're saved in CHUNKS_FOLDER, keep this False so the app shows just the
# chatbot. Set it to True to bring the tool back.
SHOW_CHUNKING_TOOL = False

# Roughly the argumentative "role" each chunk plays, guessed from its filename/id
# (e.g. "05_court_test_special_features" -> "court's reasoning"). This is just
# retrieval metadata, shown to the user for transparency in the answer below.
ROLE_BY_KEYWORD = {
    "framing": "legal test",
    "applicant": "applicant's argument",
    "commission": "commission's argument",
    "court": "court's reasoning",
}


def infer_role(filename: str) -> str:
    stem = filename.lower()
    for keyword, role in ROLE_BY_KEYWORD.items():
        if keyword in stem:
            return role
    return "unspecified"


# The 8 chunks we want out of the document, each with a short description of
# what it should contain. This is what makes the chunking "by meaning" rather
# than mechanical (e.g. splitting every N sentences): the LLM below is told
# exactly what each of these 8 chunks is supposed to be and has to find the
# matching passage itself, rather than being left to invent its own boundaries.
CHUNK_DEFINITIONS = [
    {
        "id": "01_framing_legal_test",
        "label": "Framing / legal test",
        "guidance": "The opening statement that Article 86 requires defining the relevant "
        "market from both a product standpoint and a geographic standpoint.",
    },
    {
        "id": "02_applicant_argument_interchangeability",
        "label": "Applicant's argument — interchangeability",
        "guidance": "The applicant's claim that bananas are interchangeable with other "
        "fresh fruit, including the argument about shops, shelves, prices and consumption needs.",
    },
    {
        "id": "03_applicant_evidence_seasonal_data",
        "label": "Applicant's evidence — seasonal & FAO data",
        "guidance": "The statistics and FAO studies the applicant relies on about seasonal "
        "expenditure and price effects, and the applicant's conclusion from that evidence.",
    },
    {
        "id": "04_commission_rebuttal",
        "label": "Commission's rebuttal",
        "guidance": "The Commission's argument that demand for bananas is distinct from "
        "other fruit, and that cross-price effects are too brief and spasmodic to matter.",
    },
    {
        "id": "05_court_test_special_features",
        "label": "Court's test — special features",
        "guidance": "The Court's legal test for a sufficiently differentiated market, and "
        "its findings on the banana's year-round ripening and availability.",
    },
    {
        "id": "06_court_cross_elasticity_data",
        "label": "Court's reasoning — cross-elasticity data",
        "guidance": "The Court's analysis of cross-elasticity data and the limited "
        "substitutability with oranges, apples, peaches and table grapes.",
    },
    {
        "id": "07_court_banana_characteristics",
        "label": "Court's reasoning — banana characteristics",
        "guidance": "The Court's discussion of the banana's own characteristics, the "
        "consumer groups it serves, and the FAO data on limited price impact.",
    },
    {
        "id": "08_court_conclusion",
        "label": "Court's conclusion",
        "guidance": "The Court's concluding finding that the banana market is sufficiently "
        "distinct from other fresh fruit markets.",
    },
]


def build_chunking_prompt(source_text: str) -> str:
    # Turn CHUNK_DEFINITIONS into a numbered list the model can follow, e.g.:
    # 1. id="01_framing_legal_test" — Framing / legal test: ...
    target_list = "\n".join(
        f'{i+1}. id="{c["id"]}" — {c["label"]}: {c["guidance"]}'
        for i, c in enumerate(CHUNK_DEFINITIONS)
    )
    return f"""You are splitting a legal judgment excerpt into exactly 8 pre-defined chunks.

Below is the list of the 8 target chunks, in order, each with an id and a description of what
it should contain:

{target_list}

Instructions:
- For each of the 8 target chunks above, extract the exact verbatim passage from the SOURCE
  TEXT below that matches it. Copy the original wording exactly — do not paraphrase, summarise,
  or correct anything.
- Every part of the source text should be assigned to exactly one chunk, in the order the
  chunks are listed above.
- Return ONLY valid JSON: a list of 8 objects, each with keys "id" and "text", in the same
  order as the target chunk list. No other text, no markdown code fences.

SOURCE TEXT:
{source_text}
"""


def validate_chunks(chunks: list, source_text: str) -> list[str]:
    """Sanity-check the model's output before it can be saved.

    Returns a list of problems (empty list = all good). Checks that the ids
    match our 8 targets in order, and that each chunk's text really is a
    verbatim passage of the source (ignoring whitespace differences), since an
    LLM can occasionally paraphrase or drop a sentence when asked to copy text.
    """
    def norm(s: str) -> str:
        return re.sub(r"\s+", " ", s).strip()

    problems = []
    expected_ids = [c["id"] for c in CHUNK_DEFINITIONS]
    if [c.get("id") for c in chunks] != expected_ids:
        problems.append("Chunk ids/order don't match the 8 target chunks.")

    source_norm = norm(source_text)
    for c in chunks:
        text = c.get("text")
        if not isinstance(text, str) or not text.strip():
            problems.append(f"{c.get('id')}: text is empty.")
        elif norm(text) not in source_norm:
            problems.append(f"{c.get('id')}: text is not a verbatim passage from the source.")
    return problems


# ---------------------------------------------------------------------------
# Password gate. Option 1 from the subject's security guidance: our own
# OpenAI API key stays in .env / Streamlit Cloud secrets (never committed),
# and a shared password stops a random visitor from spending our credits.
# Same approach as the class code, just reading PASSWORD instead of
# USER_PASSWORD, to match our own .env file.
# ---------------------------------------------------------------------------
APP_PASSWORD = os.environ.get("PASSWORD")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
if not APP_PASSWORD or not OPENAI_KEY:
    st.error(
        "This app isn't configured: PASSWORD and OPENAI_API_KEY must be set in "
        ".env (locally) or in the Streamlit Cloud secrets."
    )
    st.stop()

if not st.session_state.get("authenticated"):
    st.title(f"{CASE_NAME} — Relevant Market Chatbot")
    entered = st.text_input("Password", type="password")
    if entered and entered == APP_PASSWORD:
        # Remember the login for this session and rerun, so the password box
        # is no longer drawn and the app below appears.
        st.session_state.authenticated = True
        st.rerun()
    elif entered:
        st.error("Incorrect password.")
    else:
        st.info("Enter the password to access this application.")
    st.stop()

# Everything below only runs once the correct password has been entered.
api_key = OPENAI_KEY
client = OpenAI(api_key=api_key)


# ---------------------------------------------------------------------------
# Load (or create) the vector database and ingest whatever chunks are
# currently saved on disk. @st.cache_resource means this only actually runs
# once per session — later reruns (e.g. typing a new chat message) reuse the
# same `collection` object instead of re-ingesting everything from scratch.
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading knowledge base...")
def get_collection(_api_key: str):
    chroma_client = chromadb.PersistentClient(path="./my_chroma_db")

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=_api_key,
        model_name="text-embedding-3-large",
    )

    collection = chroma_client.get_or_create_collection(
        name="united_brands_relevant_market",
        embedding_function=openai_ef,
    )

    # Ingest once, silently — upsert means re-runs/redeploys are safe and
    # won't create duplicate chunks (each chunk's id is a hash of its
    # filename, so re-saving the same filename just overwrites it).
    folder = Path(CHUNKS_FOLDER)
    if folder.exists():
        files = sorted(folder.glob("*.txt"))
        documents, metadatas, ids = [], [], []
        for file in files:
            text = file.read_text(encoding="utf-8", errors="ignore").strip()
            if text:
                documents.append(text)
                metadatas.append(
                    {
                        "source": CASE_NAME,
                        "filename": file.name,
                        "role": infer_role(file.name),
                    }
                )
                ids.append(hashlib.md5(file.name.encode()).hexdigest())
        if documents:
            collection.upsert(documents=documents, metadatas=metadatas, ids=ids)

    return collection


collection = get_collection(api_key)


st.title(f"{CASE_NAME} — Relevant Market Chatbot")

# ---------------------------------------------------------------------------
# Upload & chunk a document — same shape as the class exercise (upload, then
# chunk, then save), but "chunk" here means asking an LLM to find the 8
# target passages defined above, rather than splitting every N sentences.
# Hidden behind SHOW_CHUNKING_TOOL: the chatbot further down already works
# using the chunks already included in this repository.
#
# Note: Streamlit doesn't allow an expander inside another expander, so the
# uploaded text and the individual chunks are shown with text areas /
# bordered containers instead.
# ---------------------------------------------------------------------------
if SHOW_CHUNKING_TOOL:
    with st.expander("Upload & chunk a document (optional — the chatbot below already works "
                      "with the included United Brands excerpt)"):

        # 1. Allow the user to upload a document.
        uploaded_file = st.file_uploader("Choose a file (.txt or .pdf)")

        text = None
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                if not text.strip():
                    # A scanned/image-only PDF has no text layer for pypdf to read.
                    st.warning(
                        "No text could be extracted from this PDF — it's likely a scanned "
                        "image PDF, which needs OCR first. Upload a .txt file with the "
                        "already-extracted text instead."
                    )
            else:
                text = uploaded_file.getvalue().decode("utf-8")

            if text:
                st.text_area("Uploaded text", text, height=200)

        # 2. Allow the user to chunk the document — by meaning, via an LLM call,
        # instead of a mechanical rule like "every 5 sentences".
        if text:
            if st.button("Split into the 8 target chunks"):
                with st.spinner("Asking the model to split the text by argument structure..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": build_chunking_prompt(text)}],
                        temperature=0,
                    )
                    raw = response.choices[0].message.content.strip()

                    # Guard against the model wrapping the JSON in a code fence
                    # anyway, even though we asked it not to.
                    if raw.startswith("```"):
                        raw = raw.strip("`")
                        raw = raw.split("\n", 1)[1] if "\n" in raw else raw

                    try:
                        parsed = json.loads(raw)
                        if not (
                            isinstance(parsed, list)
                            and all(isinstance(c, dict) and "id" in c and "text" in c for c in parsed)
                        ):
                            raise ValueError("Expected a list of objects with 'id' and 'text'.")
                        st.session_state["new_chunks"] = parsed
                        # Remember what we chunked, so the result can be checked
                        # against the source text on every rerun.
                        st.session_state["source_text"] = text
                    except (json.JSONDecodeError, ValueError):
                        st.error("The model didn't return the expected JSON. Raw response shown below.")
                        st.code(raw)

        # Show the chunks the model produced, one per bordered box, so they can be
        # checked before being saved.
        if "new_chunks" in st.session_state:
            new_chunks = st.session_state["new_chunks"]
            st.success(f"Produced {len(new_chunks)} chunk(s).")

            problems = validate_chunks(new_chunks, st.session_state.get("source_text", ""))
            for problem in problems:
                st.warning(problem)

            label_by_id = {c["id"]: c["label"] for c in CHUNK_DEFINITIONS}
            for chunk in new_chunks:
                label = label_by_id.get(chunk["id"], chunk["id"])
                with st.container(border=True):
                    st.markdown(f"**{chunk['id']} — {label}**")
                    st.write(chunk["text"])

            # Download the chunks as a zip, to keep on your own computer. This is
            # the way to get the files out when the app is deployed on Streamlit
            # Cloud, where files written to disk live on the server and disappear
            # when the app restarts.
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as z:
                for chunk in new_chunks:
                    z.writestr(f"{chunk['id']}.txt", chunk["text"].strip())
            st.download_button(
                "Download chunks (.zip)",
                data=buf.getvalue(),
                file_name="united_brands_chunks.zip",
                mime="application/zip",
            )

            # 3. Save each chunk of the document, and load it straight into the
            # chatbot's vector database (no app restart required).
            # Like the class code, the output folder can be chosen. Note that at
            # startup only CHUNKS_FOLDER is ingested, so if you save somewhere
            # else the chunks work for this session but not after a restart
            # (unless you also point CHUNKS_FOLDER at that location).
            output_dir = st.text_input("Output folder", value=CHUNKS_FOLDER)

            if st.button(
                "Save & load these chunks into the chatbot",
                disabled=bool(problems),
            ):
                os.makedirs(output_dir, exist_ok=True)
                documents, metadatas, ids = [], [], []
                for chunk in new_chunks:
                    filename = f"{chunk['id']}.txt"
                    filepath = os.path.join(output_dir, filename)
                    chunk_text = chunk["text"].strip()

                    # Save to disk as its own .txt file, so the chunks persist
                    # across app restarts (when running locally).
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(chunk_text)

                    documents.append(chunk_text)
                    metadatas.append(
                        {"source": CASE_NAME, "filename": filename, "role": infer_role(filename)}
                    )
                    ids.append(hashlib.md5(filename.encode()).hexdigest())

                # Upsert straight into the collection we already loaded above.
                # Same ids as get_collection() would compute (hashed from
                # filename), so this updates the existing entries in place
                # instead of duplicating them, and the chat below can use the
                # new content immediately.
                collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
                st.success(
                    f"Saved {len(new_chunks)} chunk(s) to '{output_dir}/' — the chatbot "
                    "below now uses this content."
                )


N_RESULTS = 3  # how many chunks to retrieve per question

# The chatbot's standing instructions. Sent once per question (as the
# "system" message), separately from the retrieved context and the
# conversation history that follow.
SYSTEM_PROMPT = f"""You are a legal research assistant answering questions about how the \
Court of Justice determined the relevant PRODUCT market in {CASE_NAME}.

You must answer using ONLY the retrieved excerpt(s) provided below each question — this is a \
deliberately narrow excerpt covering just the product-market reasoning (not the geographic \
market, penalties, or procedural history of the case).

Rules:
- If the retrieved excerpts do not contain the answer, say so plainly rather than using \
outside knowledge or guessing.
- If a question falls outside the scope of this excerpt (e.g. asks about the geographic \
market, fines, or other parts of the case), say that this is outside the scope of the \
document you have access to.
- Be precise and preserve the legal reasoning — do not oversimplify who argued what \
(the applicant, the Commission, or the Court's own findings)."""


# ---------------------------------------------------------------------------
# Chat UI
# ---------------------------------------------------------------------------
st.caption(
    "Ask about how the Court determined the relevant product market. "
    "Scope: product market only (this excerpt does not cover the geographic market)."
)

# Conversation memory — keeps every past message so the chat re-renders in
# full on every rerun, and so follow-up questions ("why?") make sense.
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Reset conversation"):
    st.session_state.messages = []
    st.rerun()

# Re-draw the whole conversation so far.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_question = st.chat_input("Ask a question about the relevant product market...")

if user_question:
    # Show the user's new message immediately.
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.write(user_question)

    # Retrieve the most relevant chunks for this question only — embedding
    # the whole conversation instead would blur the retrieval signal.
    results = collection.query(query_texts=[user_question], n_results=N_RESULTS)
    retrieved_docs = results["documents"][0]
    retrieved_meta = results["metadatas"][0]
    retrieved_dist = results["distances"][0]

    context = "\n\n---\n\n".join(
        f"[{meta.get('role')} | {meta.get('filename')}]\n{doc}"
        for doc, meta in zip(retrieved_docs, retrieved_meta)
    )

    # Keep a little conversation history so follow-up questions work,
    # without re-embedding the whole thread.
    history = st.session_state.messages[-6:-1]  # last few turns, excluding the one just added

    # Build the actual messages sent to the model: standing instructions,
    # then recent history, then this turn's retrieved context + question.
    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages_for_api += history
    messages_for_api.append(
        {
            "role": "user",
            "content": f"Retrieved excerpt(s):\n\n{context}\n\nQuestion: {user_question}",
        }
    )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages_for_api,
                temperature=0,
            )
        answer = response.choices[0].message.content
        st.write(answer)

        # Show which chunks were used, so the RAG mechanism is visible/
        # testable rather than a black box.
        with st.expander("Retrieved chunks used for this answer"):
            for doc, meta, dist in zip(retrieved_docs, retrieved_meta, retrieved_dist):
                st.markdown(f"**{meta.get('filename')}** · role: {meta.get('role')} · distance: {dist:.3f}")
                st.caption(doc)

    # Save the assistant's reply so it stays in the conversation history too.
    st.session_state.messages.append({"role": "assistant", "content": answer})