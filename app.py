import streamlit as st
import openai

# --- Configure OpenAI API Key ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Initialize Session State ---
if "current_section" not in st.session_state:
    st.session_state["current_section"] = "welcome"
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []  # Stores GPT conversation
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {}  # Stores user responses (profile data)

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

# --- GPT Conversational Exploration Section ---
def exploration_section():
    st.title("Exploration")
    st.subheader("Let’s explore who you are, one step at a time.")

    # Get previous messages
    messages = st.session_state["conversation"]

    # Display conversation history
    for msg in messages:
        if msg["role"] == "assistant":
            st.markdown(f"**Euripides:** {msg['content']}")
        else:
            st.markdown(f"**You:** {msg['content']}")

    # User input
    user_input = st.text_input("Your response:", key="user_input")

    if st.button("Send"):
        if user_input:
            # Append user input to conversation
            messages.append({"role": "user", "content": user_input})
            st.session_state["conversation"] = messages

            # Send to GPT
            with st.spinner("Euripides is thinking..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are Euripides, a personal branding assistant. Help users explore their identity, passions, and professional goals."},
                        *messages,  # Send full conversation context
                    ]
                )
                gpt_reply = response["choices"][0]["message"]["content"]

            # Append GPT response to conversation
            messages.append({"role": "assistant", "content": gpt_reply})
            st.session_state["conversation"] = messages

# --- Insights Section Placeholder ---
def insights_section():
    st.title("Insights")
    st.subheader("Here’s what we’ve uncovered about you!")

    # Placeholder for generating insights
    st.markdown("Insights will be generated here based on your exploration data.")

    if st.button("Restart"):
        st.session_state["current_section"] = "welcome"
        st.session_state["conversation"] = []
        st.session_state["user_profile"] = {}

# --- Main App Logic ---
if st.session_state["current_section"] == "welcome":
    welcome_section()
elif st.session_state["current_section"] == "exploration":
    exploration_section()
elif st.session_state["current_section"] == "insights":
    insights_section()
