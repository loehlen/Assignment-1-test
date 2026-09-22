import streamlit as st


# --------------------------------------------------
# Page title
# --------------------------------------------------

st.title("United Brands v Commission")
st.subheader("Understanding the Relevant Product Market")


# --------------------------------------------------
# Introduction
# --------------------------------------------------

st.write(
    """
    In competition law, determining the relevant market is an important
    first step in assessing a company's market power.
    """
)

st.write(
    """
    This application demonstrates this process through
    *United Brands v Commission* (Case 27/76). While the judgment
    addresses a broader set of issues, this application focuses specifically
    on the Court's analysis of the relevant product market in paragraphs 10–35.
    """
)


# --------------------------------------------------
# Interactive introduction
# --------------------------------------------------

st.divider()

st.subheader("Before looking at the case")


if "intro_topic" not in st.session_state:
    st.session_state.intro_topic = None


col1, col2 = st.columns(2)

with col1:

    if st.button(
        "Why do I need the relevant market?",
        use_container_width=True
    ):
        st.session_state.intro_topic = "why"


with col2:

    if st.button(
        "What is the question in United Brands?",
        use_container_width=True
    ):
        st.session_state.intro_topic = "question"


if st.session_state.intro_topic == "why":

    st.info(
        """
        In United Brands, the Court explained that the relevant market
        had to be defined in order to determine whether United Brands
        held a dominant position.

        The market had to be considered from both the product and
        geographic points of view. This application focuses on the
        relevant product market.
        """
    )

    st.caption("Paragraphs 10–11")


elif st.session_state.intro_topic == "question":

    st.info(
        """
        The relevant product-market question was whether bananas were
        reasonably interchangeable with other fresh fruit, or whether
        the banana market was sufficiently distinct from other fresh
        fruit markets.
        """
    )

    st.caption("Paragraph 12")


# --------------------------------------------------
# Court's analysis
# --------------------------------------------------

st.divider()

st.subheader("Follow the Court's analysis")

st.write(
    """
    The judgment develops this question through the arguments of the
    parties and the Court's subsequent assessment.
    """
)


if "analysis_step" not in st.session_state:
    st.session_state.analysis_step = 1


# Step buttons

step1, step2, step3, step4 = st.columns(4)


with step1:

    if st.button(
        "1. Applicant",
        use_container_width=True
    ):
        st.session_state.analysis_step = 1


with step2:

    if st.button(
        "2. Evidence",
        use_container_width=True
    ):
        st.session_state.analysis_step = 2


with step3:

    if st.button(
        "3. Commission",
        use_container_width=True
    ):
        st.session_state.analysis_step = 3


with step4:

    if st.button(
        "4. Court",
        use_container_width=True
    ):
        st.session_state.analysis_step = 4


# --------------------------------------------------
# Selected step
# --------------------------------------------------

st.write("")


if st.session_state.analysis_step == 1:

    st.markdown("### The applicant's argument")

    st.write(
        """
        The applicant argued that bananas were reasonably interchangeable
        with other kinds of fresh fruit.

        It pointed to the fact that bananas and other fresh fruit were
        sold in the same shops and displayed on the same shelves, had
        comparable prices, and satisfied the same consumer needs.
        """
    )

    st.caption("Paragraphs 12–13")


elif st.session_state.analysis_step == 2:

    st.markdown("### The evidence relied upon by the applicant")

    st.write(
        """
        The applicant relied on statistics and FAO studies concerning
        seasonal price movements and consumer expenditure.

        It argued that this evidence supported treating bananas and
        other fresh fruit as part of the same market.
        """
    )

    st.caption("Paragraphs 14–18")


elif st.session_state.analysis_step == 3:

    st.markdown("### The Commission's response")

    st.write(
        """
        The Commission argued that the demand for bananas was distinct
        from the demand for other fresh fruit.

        It relied on the particular qualities of bananas and argued that
        the effects of other fruit on banana prices and availability were
        ineffective, brief or spasmodic.
        """
    )

    st.caption("Paragraphs 19–21")


elif st.session_state.analysis_step == 4:

    st.markdown("### The Court's assessment and conclusion")

    st.write(
        """
        The Court examined whether bananas were sufficiently interchangeable
        with other fresh fruit. It considered their characteristics,
        year-round availability, seasonal substitutability and evidence
        concerning the degree of substitutability.

        Taking these factors together, the Court concluded that the banana
        market was sufficiently distinct from the other fresh fruit markets.
        """
    )

    st.caption("Paragraphs 22–35")


# --------------------------------------------------
# Chatbot
# --------------------------------------------------

st.divider()

st.subheader("Explore the judgment")

st.write(
    """
    You can now use the chatbot to ask questions about the arguments,
    evidence and reasoning contained in paragraphs 10–35.
    """
)


if st.button("Go to the chatbot →"):

    st.switch_page("home.py")