import streamlit as st


st.title("United Brands v Commission")
st.subheader("Understanding the Relevant Product Market")


# --------------------------------------------------
# Short introduction
# --------------------------------------------------

st.write(
    """
    In competition law, defining the relevant market is an important
    first step in assessing a company's market power.
    """
)

st.write(
    """
    This application demonstrates this process through
    *United Brands v Commission* (Case 27/76). While the judgment
    addresses a broader set of issues, this application focuses
    specifically on the Court's analysis of the relevant product
    market in paragraphs 10–35.
    """
)


# --------------------------------------------------
# 1. Why do we need the relevant market?
# --------------------------------------------------

st.divider()

st.subheader("Before looking at the case")

if "intro_topic" not in st.session_state:
    st.session_state.intro_topic = None


if st.button(
    "Why do I need the relevant market?",
    use_container_width=True
):
    st.session_state.intro_topic = "why"


if st.session_state.intro_topic == "why":

    st.info(
        """
        In order to determine whether a company holds a dominant position,
        the relevant market first has to be defined.

        The market must be considered from both the product and geographic
        points of view. This application focuses on the relevant product
        market.
        """
    )

    st.caption("Paragraphs 10–11")


# --------------------------------------------------
# 2. What was the question in United Brands?
# --------------------------------------------------

if st.button(
    "What was the relevant product-market question?",
    use_container_width=True
):
    st.session_state.intro_topic = "question"


if st.session_state.intro_topic == "question":

    st.info(
        """
        Did bananas form part of the broader market for fresh fruit,
        or did bananas constitute a sufficiently distinct market of
        their own?

        The Court approached this question by examining whether bananas
        were reasonably interchangeable with other fresh fruit.
        """
    )

    st.caption("Paragraph 12")


# --------------------------------------------------
# 3. The opposing views
# --------------------------------------------------

st.divider()

st.subheader("The opposing views")

st.write(
    """
    The applicant and the Commission took different positions on
    whether bananas belonged to the same market as other fresh fruit.
    """
)


left, right = st.columns(2)


with left:

    st.markdown("### Applicant's argument")

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


with right:

    st.markdown("### Commission's response")

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


# --------------------------------------------------
# 4. What did the Court decide?
# --------------------------------------------------

st.divider()

st.subheader("What did the Court decide?")

st.write(
    """
    The Court examined whether bananas were sufficiently interchangeable
    with other fresh fruit. It considered their characteristics,
    year-round availability, seasonal substitutability and evidence
    concerning the degree of substitutability.
    """
)

st.write(
    """
    Taking these factors together, the Court concluded that the banana
    market was sufficiently distinct from the other fresh fruit markets.
    """
)

st.caption("Paragraphs 22–35")


# --------------------------------------------------
# 5. Explore the judgment
# --------------------------------------------------

st.divider()

st.subheader("Explore the Court's reasoning")

st.write(
    """
    The chatbot allows you to explore the arguments, evidence and
    reasoning contained in paragraphs 10–35 of the judgment.
    """
)


if st.button("Go to the chatbot →"):

    st.switch_page("home.py")