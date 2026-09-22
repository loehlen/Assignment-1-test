import streamlit as st


st.title("United Brands v Commission")
st.subheader("Understanding the Relevant Product Market")


st.write(
    """
    In competition law, determining the relevant market is an important
    first step in assessing a company's market power. The relevant market
    defines the products and geographic area within which a company competes,
    providing the basis for assessing its position in the market.
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

st.write(
    """
    The central question in this part of the judgment was whether
    **bananas belonged to the broader market for fresh fruit or constituted
    a separate relevant product market.**
    """
)


st.divider()

st.subheader("Follow the Court's analysis")


with st.expander("1. The applicant's argument"):

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


with st.expander("2. The evidence relied upon by the applicant"):

    st.write(
        """
        The applicant also relied on statistics and FAO studies concerning
        seasonal price movements and consumer expenditure.

        It argued that this evidence supported treating bananas and other
        fresh fruit as part of the same market.
        """
    )

    st.caption("Paragraphs 14–18")


with st.expander("3. The Commission's response"):

    st.write(
        """
        The Commission argued that the demand for bananas was distinct
        from the demand for other fresh fruit.

        It relied on the particular qualities of bananas and argued that
        the effects of other fruit on banana demand were ineffective,
        brief or spasmodic.
        """
    )

    st.caption("Paragraphs 19–21")


with st.expander("4. The Court's assessment and conclusion"):

    st.write(
        """
        The Court examined whether bananas were sufficiently interchangeable
        with other fresh fruit. It considered their characteristics,
        year-round availability, seasonal substitutability and evidence
        concerning cross-elasticity of demand.

        The Court ultimately found that other fresh fruit did not exert
        sufficient competitive pressure on bananas and concluded that
        the banana market was sufficiently distinct.
        """
    )

    st.caption("Paragraphs 22–35")


st.divider()

st.subheader("Explore the judgment")

st.write(
    """
    You can now use the chatbot to explore the arguments, evidence and
    reasoning contained in paragraphs 10–35 of the judgment.
    """
)


if st.button("Go to the chatbot"):
    st.switch_page("home.py")