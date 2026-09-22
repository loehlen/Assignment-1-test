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


    # -----------------------------------------------------------------------
    # Case introduction
    # -----------------------------------------------------------------------

    st.title(
        "United Brands v Commission"
    )

    st.subheader(
        "Understanding the Relevant Product Market"
    )

    st.write(
        """
        In United Brands v Commission (Case 27/76), the Court had to
        define the relevant market in order to determine whether United
        Brands held a dominant position.

        One central question was whether bananas formed part of a broader
        market for fresh fruit or whether the banana market was sufficiently
        distinct from other fresh fruit markets.

        This application focuses on paragraphs 10–35 of the judgment,
        which deal with the relevant product market.
        """
    )


    # -----------------------------------------------------------------------
    # What the application covers
    # -----------------------------------------------------------------------

    st.subheader("What does this application cover?")

    st.write(
        """
        • The definition of the relevant product market

        • The applicant's arguments

        • The Commission's response

        • The evidence concerning substitutability

        • The Court's assessment

        • The Court's conclusion
        """
    )


    with st.expander("What is outside the scope?"):

        st.write(
            """
            • The geographic market

            • The assessment of dominance beyond the market-definition issue

            • Penalties

            • Other parts of the judgment
            """
        )


    # -----------------------------------------------------------------------
    # Central question
    # -----------------------------------------------------------------------

    st.subheader("The central question")

    st.info(
        "Are bananas part of the broader fresh fruit market, "
        "or do they constitute a separate relevant product market?"
    )

    st.write(
        """
        To answer this question, the Court considered whether bananas
        were sufficiently interchangeable with other fresh fruit and
        examined the circumstances affecting the degree of competition
        between them.
        """
    )


    # -----------------------------------------------------------------------
    # Follow the Court's analysis
    # -----------------------------------------------------------------------

    st.subheader("Follow the Court's analysis")

    st.write(
        """
        The judgment develops this question through a series of arguments
        and findings. Explore the steps below to understand how the
        relevant product market was determined.
        """
    )


    with st.expander("1 — Define the market"):

        st.write(
            "Why did the Court need to define the relevant market "
            "in the first place?"
        )


    with st.expander("2 — The applicant's argument"):

        st.write(
            "Why did the applicant argue that bananas belonged "
            "to the broader fresh fruit market?"
        )


    with st.expander("3 — The evidence"):

        st.write(
            "What did the statistics and FAO studies show about "
            "the relationship between bananas and other fresh fruit?"
        )


    with st.expander("4 — The Commission's response"):

        st.write(
            "Why did the Commission consider the demand for bananas "
            "to be distinct?"
        )


    with st.expander("5 — The Court's assessment"):

        st.write(
            "What factors did the Court consider when assessing "
            "whether bananas were interchangeable with other fresh fruit?"
        )


    with st.expander("6 — The conclusion"):

        st.write(
            "Why did the Court conclude that the banana market "
            "was sufficiently distinct?"
        )


    # -----------------------------------------------------------------------
    # Chatbot UI
    # -----------------------------------------------------------------------

    st.subheader("Explore the case")

    st.write(
        "Ask questions about the Court's approach to defining "
        "the relevant product market."
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
        with st.expander("Sources used for this answer"):

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