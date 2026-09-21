import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
import hashlib
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Password
if "password" not in st.session_state:
    st.session_state.password = ""

st.session_state.password = st.text_input(
    label="password",
    type="password"
)

if st.session_state.password == os.environ["PASSWORD"]:

    os.environ["CHROMA_OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

    CASE_NAME = "United Brands v Commission (Case 27/76)"

    CHUNKS_FOLDER = (
        "Chunks - United Brands v Commission - Relevant Product Market"
    )

    @st.cache_resource
    def get_collection():

        client = chromadb.PersistentClient(
            path="./my_chroma_db"
        )

        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            model_name="text-embedding-3-large",
        )

        collection = client.get_or_create_collection(
            name="united_brands_relevant_market",
            embedding_function=openai_ef,
        )

        # Ingest the prepared chunks
        folder = Path(CHUNKS_FOLDER)

        if folder.exists():

            files = sorted(folder.glob("*.txt"))

            documents, metadatas, ids = [], [], []

            for file in files:

                text = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).strip()

                if text:

                    documents.append(text)

                    metadatas.append({
                        "source": CASE_NAME,
                        "filename": file.name
                    })

                    ids.append(
                        hashlib.md5(
                            file.name.encode()
                        ).hexdigest()
                    )

            if documents:

                collection.upsert(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )

        return collection


    collection = get_collection()


    # --- Chatbot UI ---

    st.title(
        "United Brands v Commission — Relevant Market Chatbot"
    )

    st.caption(
        "Ask questions about how the Court determined the relevant "
        "product market. The chatbot covers paragraphs 10–35 only."
    )


    # --- Conversation history ---

    if "messages" not in st.session_state:
        st.session_state.messages = []


    if st.sidebar.button("Reset conversation"):
        st.session_state.messages = []
        st.rerun()


    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])


    # --- Search / RAG response ---

    query = st.chat_input(
        "Ask a question about the relevant product market..."
    )

    n_results = 3

    client = OpenAI()


    if query:

        # Show user question
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):
            st.write(query)


        # Retrieve relevant chunks
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )


        # Show retrieved chunks
        with st.expander("Retrieved chunks used for this answer"):

            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            ):

                st.markdown(
                    f"**{meta.get('filename')}** "
                    f"· distance: {dist:.3f}"
                )

                st.caption(doc)


        # Use retrieved chunks as context for a RAG response
        context = "\n\n---\n\n".join(
            results["documents"][0]
        )


        # System instructions
        system_prompt = f"""
You are a legal research assistant answering questions about how the
Court of Justice determined the relevant PRODUCT market in {CASE_NAME}.

Use only the retrieved context provided below.

The available material covers paragraphs 10–35 of the judgment and
concerns the relevant product market. It does not cover the geographic
market or other parts of the case.

If the context does not contain the answer, say so. Do not make anything up.

Be precise about who is making an argument. Distinguish between:
- the applicant's arguments,
- the Commission's arguments, and
- the Court's own reasoning and findings.

Do not use outside knowledge.
"""


        # Keep recent conversation history
        history = st.session_state.messages[-6:-1]


        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages += history

        messages.append(
            {
                "role": "user",
                "content": f"""
Retrieved context:

{context}

Question:

{query}
"""
            }
        )


        # Generate RAG response
        with st.chat_message("assistant"):

            with st.spinner("Generating response..."):

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0,
                )

            answer = response.choices[0].message.content

            st.write(answer)


        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )