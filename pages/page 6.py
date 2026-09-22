import streamlit as st


# --------------------------------------------------
# Page styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    /* Main buttons */
    div.stButton > button {
        border: 1px solid #E8CDD4;
        border-radius: 8px;
        background-color: white;
        color: #30313D;
    }

    div.stButton > button:hover {
        border-color: #D8B3BE;
        background-color: #F5E6EA;
        color: #30313D;
    }

    /* Primary (continue / go-to-chatbot) button */
    div.stButton > button[kind="primary"] {
        border: 1px solid #9B6574;
        background-color: #9B6574;
        color: white;
    }

    div.stButton > button[kind="primary"]:hover {
        border-color: #85526035;
        background-color: #85525F;
        color: white;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        border: 1px solid #E2D9DC;
        border-radius: 8px;
    }

    /* Small paragraph references */
    .paragraph-reference {
        color: #8A7C81;
        font-size: 0.85rem;
        margin-top: 0.2rem;
    }

    /* Step progress indicator */
    .step-indicator {
        color: #9B6574;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    /* Hook / teaser line above an expander */
    .teaser {
        font-size: 1.02rem;
        color: #4A4A52;
        margin-bottom: 0.6rem;
    }

    /* Conclusion / court-holding box, in the same palette as the rest */
    .conclusion-box {
        background-color: #F5E6EA;
        border: 1px solid #E8CDD4;
        border-left: 4px solid #9B6574;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        color: #30313D;
        margin: 1rem 0;
    }

    .conclusion-box strong {
        color: #9B6574;
    }

    /* Slim progress bar in the theme color */
    div[data-testid="stProgress"] div[role="progressbar"] > div {
        background-color: #9B6574;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Step state
# --------------------------------------------------

TOTAL_STEPS = 5

if "intro_step" not in st.session_state:
    st.session_state.intro_step = 1


def go_next():
    st.session_state.intro_step = min(st.session_state.intro_step + 1, TOTAL_STEPS)


def go_back():
    st.session_state.intro_step = max(st.session_state.intro_step - 1, 1)


# --------------------------------------------------
# Title (shown throughout)
# --------------------------------------------------

st.title("United Brands v Commission")
st.subheader("Understanding the Relevant Product Market")

# Intro copy only shows on the first step, before the walkthrough begins
if st.session_state.intro_step == 1:
    st.write(
        """
        Was Chiquita's banana business operating in a market of its own —
        or just one player among many in the broader fresh fruit market?
        """
    )

    st.write(
        """
        Before competition law can assess a company's market power, it first
        has to answer that kind of question: **what market is the company
        actually competing in?** *United Brands v Commission* (Case 27/76)
        shows the Court working through exactly this problem. While the
        judgment covers a broader set of issues, this application focuses
        specifically on the Court's analysis of the relevant product market
        in paragraphs 10–35.
        """
    )

st.divider()

st.markdown(
    f'<div class="step-indicator">Step {st.session_state.intro_step} of {TOTAL_STEPS}</div>',
    unsafe_allow_html=True
)
st.progress(st.session_state.intro_step / TOTAL_STEPS)


# --------------------------------------------------
# Step 1 — The relevant market
# --------------------------------------------------

if st.session_state.intro_step == 1:

    st.header("The relevant market")

    st.markdown(
        '<div class="teaser">Before asking whether a company is dominant, '
        'the law needs a baseline: dominant over <em>what</em>, exactly?</div>',
        unsafe_allow_html=True
    )

    with st.expander("Why do I need the relevant market?", expanded=True):

        st.write(
            """
            In order to determine whether a company holds a dominant position,
            the relevant market first has to be defined.

            The market must be considered from both the product and geographic
            points of view. This application focuses on the relevant product
            market.
            """
        )

        st.markdown(
            '<div class="paragraph-reference">Paragraphs 10–11</div>',
            unsafe_allow_html=True
        )


# --------------------------------------------------
# Step 2 — The market-definition question
# --------------------------------------------------

elif st.session_state.intro_step == 2:

    st.header("The market-definition question")

    st.markdown(
        '<div class="teaser">So which is it — bananas as one fruit among '
        'many, or bananas as their own market?</div>',
        unsafe_allow_html=True
    )

    with st.expander("What exactly did the Court have to determine?", expanded=True):

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

        st.markdown(
            '<div class="paragraph-reference">Paragraph 12</div>',
            unsafe_allow_html=True
        )


# --------------------------------------------------
# Step 3 — The opposing views
# --------------------------------------------------

elif st.session_state.intro_step == 3:

    st.header("The opposing views")

    st.write(
        """
        The applicant and the Commission took different positions on whether
        bananas belonged to the same market as other fresh fruit.
        """
    )

    left, right = st.columns(2)

    with left:

        with st.expander("Applicant's argument", expanded=True):

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

            st.markdown(
                '<div class="paragraph-reference">Paragraphs 12–13</div>',
                unsafe_allow_html=True
            )

    with right:

        with st.expander("Commission's response", expanded=True):

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

            st.markdown(
                '<div class="paragraph-reference">Paragraphs 19–21</div>',
                unsafe_allow_html=True
            )


# --------------------------------------------------
# Step 4 — The Court's assessment
# --------------------------------------------------

elif st.session_state.intro_step == 4:

    st.header("The Court's assessment")

    st.write("How did the Court work through these competing arguments?")

    with st.expander("The Court's market-definition approach"):

        st.write(
            """
            The Court examined whether bananas were sufficiently interchangeable
            with other fresh fruit and whether there was a sufficiently distinct
            market for bananas.
            """
        )

        st.markdown(
            '<div class="paragraph-reference">Paragraphs 22–27</div>',
            unsafe_allow_html=True
        )

    with st.expander("Substitutability between bananas and other fruit"):

        st.write(
            """
            The Court examined whether other fresh fruit could exert sufficient
            competitive pressure on bananas.

            It considered seasonal substitutability and evidence concerning
            the degree of substitutability.
            """
        )

        st.markdown(
            '<div class="paragraph-reference">Paragraphs 28–30</div>',
            unsafe_allow_html=True
        )

    with st.expander("Characteristics of bananas and consumer choice"):

        st.write(
            """
            The Court also considered the particular characteristics of bananas,
            including their appearance, taste, softness, seedlessness and ease
            of handling, as well as their year-round availability.

            These characteristics were relevant to the Court's assessment of
            whether consumers would switch to other fresh fruit.
            """
        )

        st.markdown(
            '<div class="paragraph-reference">Paragraphs 31–33</div>',
            unsafe_allow_html=True
        )

    with st.expander("The Court's overall conclusion"):

        st.write(
            """
            Taking these factors together, the Court concluded that a very large
            number of consumers were not noticeably or appreciably induced to
            switch from bananas to other fresh fruit.

            The banana market was therefore sufficiently distinct from the
            other fresh fruit markets.
            """
        )

        st.markdown(
            '<div class="paragraph-reference">Paragraphs 34–35</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="conclusion-box">
        <strong>Conclusion:</strong> the Court held that the banana market was
        sufficiently distinct from the other fresh fruit markets.
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Step 5 — Explore the judgment
# --------------------------------------------------

elif st.session_state.intro_step == 5:

    st.header("Explore the market-definition analysis")

    st.write(
        """
        The chatbot lets you dig deeper into any of the arguments, evidence
        or reasoning covered above — ask it to explain a step, compare the
        parties' positions, or point you to a specific paragraph in
        paragraphs 10–35 of the judgment.
        """
    )


# --------------------------------------------------
# Navigation
# --------------------------------------------------

st.write("")
nav_back, nav_spacer, nav_next = st.columns([1, 3, 1])

with nav_back:
    st.button(
        "← Back",
        on_click=go_back,
        disabled=(st.session_state.intro_step == 1),
        use_container_width=True,
    )

with nav_next:
    if st.session_state.intro_step < TOTAL_STEPS:
        st.button(
            "Continue →",
            on_click=go_next,
            type="primary",
            use_container_width=True,
        )
    else:
        if st.button("Go to the chatbot →", type="primary", use_container_width=True):
            st.switch_page("home.py")