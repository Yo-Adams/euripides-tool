import streamlit as st
import openai

# --- Configure OpenAI API Key ---
openai.api_key = st.secrets "OPENAI_API_KEY"

# --- Initialize Session State ---
if "current_section" not in st.session_state:
    st.session_state["current_section"] = "welcome"

if "user_data" not in st.session_state:
    st.session_state["user_data"] = {}

# --- Welcome Section ---
def welcome_section():
    st.title("Welcome to Euripides!")
    st.subheader("Your personal Deus Ex Machina for crafting your digital presence.")
    st.markdown("""
    Euripides is here to help you explore who you are and craft actionable insights for building your digital presence. Let's get started!
    """)

    # Collect user's preferred name
    user_name = st.text_input("What should I call you?", placeholder="Enter your name")
    st.session_state["user_data"]["name"] = user_name

    # Navigation to next section
    if st.button("Start Exploration"):
        st.session_state["current_section"] = "exploration"

# --- Exploration Section ---
def exploration_section():
    st.title("Exploration")
    st.subheader("Let’s dive into who you are and what you care about!")

    # Collect Core Identity
    st.session_state["user_data"]["core_identity"] = st.text_area(
        "What values guide your decisions?",
        placeholder="E.g., authenticity, creativity, community..."
    )

    # Collect Passions
    st.session_state["user_data"]["passions"] = st.text_area(
        "What activities or topics make you lose track of time?",
        placeholder="E.g., photography, cooking, hiking..."
    )

    # Collect Professional Background
    st.session_state["user_data"]["professional"] = st.text_area(
        "Tell me about your current role and the skills you bring.",
        placeholder="E.g., marketing director, skilled in storytelling and analytics..."
    )

    # Navigation to Insights Section
    if st.button("Generate Insights"):
        st.session_state["current_section"] = "insights"

# --- Insights Section ---
def insights_section():
    st.title("Insights")
    st.subheader("Here’s what we’ve uncovered about you!")

    # Format user data for GPT
    exploration_data = f"""
    Name: {st.session_state['user_data'].get('name', 'Anonymous')}
    Core Identity: {st.session_state['user_data'].get('core_identity', 'Not provided')}
    Passions: {st.session_state['user_data'].get('passions', 'Not provided')}
    Professional Background: {st.session_state['user_data'].get('professional', 'Not provided')}
    """

    # System prompt for GPT
    system_prompt = """
    You are Euripides, a personal branding assistant. Based on the user data provided, summarize their persona and suggest actionable strategies for building their digital presence.
    """

    # Send data to GPT
    with st.spinner("Generating insights..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": exploration_data},
            ]
        )
        gpt_reply = response["choices"][0]["message"]["content"]

    # Display GPT-generated insights
    st.markdown(gpt_reply)

    # Offer next steps
    if st.button("Restart"):
        st.session_state["current_section"] = "welcome"

# --- Main App Logic ---
if st.session_state["current_section"] == "welcome":
    welcome_section()
elif st.session_state["current_section"] == "exploration":
    exploration_section()
elif st.session_state["current_section"] == "insights":
    insights_section()
