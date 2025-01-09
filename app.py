import streamlit as st
import openai

# --- Configure OpenAI API Key (Hardcoded) ---
openai.api_key = "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"

# --- Initialize Session State ---
if "current_section" not in st.session_state:
    st.session_state["current_section"] = "welcome"
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []  # Stores GPT conversation
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {}  # Stores user responses

# --- Welcome Section ---
def welcome_section():
    st.title("Welcome to Euripides!")
    st.subheader("Your personal Deus Ex Machina for crafting your digital presence.")
    st.markdown("""
    Euripides is here to help you explore who you are and craft actionable insights for building your digital presence. Let's get started!
    """)

    # Collect user's preferred name
    user_name = st.text_input("What should I call you?", placeholder="Enter your name")
    st.session_state["user_profile"]["name"] = user_name

    # Collect user's reason for using the tool
    user_goal = st.radio(
        "What brings you here today?",
        options=["Explore who I am", "Build my digital presence", "Discover my audience", "Other"],
    )
    st.session_state["user_profile"]["goal"] = user_goal

    # Collect user's energy level
    energy_level = st.slider(
        "How are you feeling today? (1 = Low Energy, 10 = High Energy)",
        min_value=1,
        max_value=10,
        value=5,
    )
    st.session_state["user_profile"]["energy"] = energy_level

    # Navigation to next section
    if st.button("Start Exploration"):
        st.session_state["current_section"] = "exploration"
        st.session_state["conversation"] = [
            {"role": "assistant", "content": "Welcome! Let’s start by understanding more about you. What values guide your decisions?"}
        ]

# --- GPT Conversational Section ---
def conversational_section():
    st.title("Exploration")
    st.subheader("Let’s explore who you are, one step at a time.")

    # Display conversation history
    for msg in st.session_state["conversation"]:
        if msg["role"] == "assistant":
            st.markdown(f"**Euripides:** {msg['content']}")
        else:
            st.markdown(f"**You:** {msg['content']}")

    # User input
    user_input = st.text_input("Your response:", key="user_input")

    if st.button("Send"):
        if user_input.strip():
            # Append user input to conversation
            st.session_state["conversation"].append({"role": "user", "content": user_input})

            # Send updated conversation to GPT
            with st.spinner("Euripides is thinking..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are Euripides, a conversational assistant helping users explore their identity, passions, and goals."},
                        *st.session_state["conversation"],  # Include the full conversation so far
                    ]
                )
                gpt_reply = response["choices"][0]["message"]["content"]

            # Append GPT response to conversation
            st.session_state["conversation"].append({"role": "assistant", "content": gpt_reply})

            # Check if user is ready to proceed to Insights
            if "ready for insights" in gpt_reply.lower():
                st.session_state["current_section"] = "insights"

# --- Insights Section ---
def insights_section():
    st.title("Insights")
    st.subheader("Here’s what we’ve uncovered about you!")

    # Summarize conversation into actionable insights
    with st.spinner("Generating insights..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Euripides, a branding assistant. Provide actionable insights based on this conversation."},
                *st.session_state["conversation"],
            ]
        )
        insights = response["choices"][0]["message"]["content"]

    # Display GPT-generated insights
    st.markdown(insights)

    # Offer option to restart
    if st.button("Restart"):
        st.session_state["current_section"] = "welcome"
        st.session_state["conversation"] = []
        st.session_state["user_profile"] = {}

# --- Main App Logic ---
if st.session_state["current_section"] == "welcome":
    welcome_section()
elif st.session_state["current_section"] == "exploration":
    conversational_section()
elif st.session_state["current_section"] == "insights":
    insights_section()
