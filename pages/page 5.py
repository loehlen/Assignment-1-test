import streamlit as st


st.title("United Brands v Commission")
st.subheader("Understanding the Relevant Product Market")


# --------------------------------------------------
# Introduction
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
# 1. Before looking at the case
# --------------------------------------------------

st.divider()

st.subheader("Before looking at the case")


with st.expander("Why do I need the relevant market?"):

    st.write(
        """
        In order to determine whether a company holds a dominant position,
        the relevant market first has to be defined.

        The market must be considered from both the product and geographic
        points of view. This application focuses on the relevant product
        market.
        """
    )

    st.caption("Paragraphs 10–11")


with st.expander("What was the relevant product-market question?"):

    st.write(
        """
        Did bananas form part of the broader market for fresh fruit,
        or did bananas constitute a sufficiently distinct market of
        their own?
        """
    )

    st.write(
        """
        The Court approached this question by examining whether bananas
        were reasonably interchangeable with other fresh fruit.
        """
    )

    st.caption("Paragraph 12")


# --------------------------------------------------
# 2. The opposing views
# --------------------------------------------------

st.divider()

st.subheader("The opposing views")

st.write(
    """
    The applicant and the Commission took different positions on whether
    bananas belonged to the same market as other fresh fruit.
    """
)


left, right = st.columns(2)


with left:

    with st.expander("Applicant's argument"):

        st.write(
            """
            The applicant argued that bananas were reasonably
            interchangeable with other kinds of fresh fruit.
            """
        )

        st.write(
            """
            It pointed to the fact that bananas and other fresh fruit
            were sold in the same shops and displayed on the same shelves,
            had comparable prices, and satisfied the same consumer needs.
            """
        )

        st.caption("Paragraphs 12–13")


with right:

    with st.expander("Commission's response"):

        st.write(
            """
            The Commission argued that the demand for bananas was distinct
            from the demand for other fresh fruit.
            """
        )

        st.write(
            """
            It relied on the particular qualities of bananas and argued
            that the effects of other fruit on banana prices and availability
            were ineffective, brief or spasmodic.
            """
        )

        st.caption("Paragraphs 19–21")


# --------------------------------------------------
# 3. What did the Court decide?
# --------------------------------------------------

st.divider()

st.subheader("What did the Court decide?")


with st.expander(
    "The Court concluded that the banana market was sufficiently distinct"
):

    st.write(
        """
        The Court concluded that bananas constituted a market sufficiently
        distinct from the other fresh fruit markets.
        """
    )

    st.caption("Paragraphs 34–35")


# --------------------------------------------------
# 4. How did the Court reach its conclusion?
# --------------------------------------------------

st.subheader("How did the Court reach its conclusion?")


with st.expander("1. The Court's market-definition test"):

    st.write(
        """
        The Court considered whether there was a sufficiently distinct
        market for bananas based on the degree of interchangeability
        between bananas and other fresh fruit.
        """
    )

    st.caption("Paragraphs 22–27")


with st.expander("2. Substitutability between bananas and other fruit"):

    st.write(
        """
        The Court examined whether other fresh fruit could exert sufficient
        competitive pressure on bananas.

        It considered seasonal substitutability and evidence concerning
        cross-elasticity of demand.
        """
    )

    st.caption("Paragraphs 28–30")


with st.expander("3. Characteristics of bananas and consumer choice"):

    st.write(
        """
        The Court also considered the particular characteristics of bananas,
        including their appearance, taste, softness, seedlessness and ease
        of handling, as well as their year-round availability.

        These characteristics were relevant to the Court's assessment of
        whether consumers would switch to other fresh fruit.
        """
    )

    st.caption("Paragraphs 31–33")


# --------------------------------------------------
# 5. Explore the judgment
# --------------------------------------------------

st.divider()

st.subheader("Explore the market-definition analysis")

st.write(
    """
    The chatbot allows you to explore the arguments, evidence and
    reasoning contained in paragraphs 10–35 of the judgment.
    """
)


if st.button("Go to the chatbot →"):

    st.switch_page("home.py")