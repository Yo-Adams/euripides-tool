import streamlit as st
import openai

# --- Configure OpenAI API Key (Hardcoded) ---
openai.api_key = "your-new-api-key"

# --- Initialize Session State ---
if "current_section" not in st.session_state:
    st.session_state["current_section"] = "welcome"
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []  # Stores chat history
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {}  # Stores user data

# --- Welcome Section ---
def welcome_section():
    st.title("Euripides")
    st.subheader("Your personal Deus Ex Machina for crafting your digital presence.")
    st.markdown("""
    **Euripides** helps you explore who you are and craft actionable insights to build an authentic digital presence. Let’s start your journey.
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

    # Collect user's energy level with dynamic feedback
    energy_level = st.slider(
        "How are you feeling today? (1 = Low Energy, 10 = High Energy)",
        min_value=1,
        max_value=10,
        value=5,
    )
    energy_feedback = "Feeling energetic!" if energy_level > 7 else (
        "Let's take it easy today." if energy_level < 4 else "Ready to dive in!"
    )
    st.markdown(f"**Feedback:** {energy_feedback}")
    st.session_state["user_profile"]["energy"] = energy_level

    # CTA: Start Talking to Euripides
    if st.button("Start Talking to Euripides"):
        st.session_state["current_section"] = "chat"
        st.session_state["conversation"] = [
            {"role": "assistant", "content": f"Hi {user_name}! I'm Euripides. Let's start with what values guide your decisions?"}
        ]

# --- Chat Interface Section ---
def chat_interface():
    st.title("Euripides: Your Digital Presence Assistant")
    st.markdown("Chat with Euripides to uncover insights about your passions, goals, and professional identity.")

    # Display chat history
    for message in st.session_state["conversation"]:
        if message["role"] == "assistant":
            st.markdown(f"**Euripides:** {message['content']}")
        else:
            st.markdown(f"**You:** {message['content']}")

    # Input box for user response
    user_input = st.text_input("Type your message here:", key="user_input")

    if st.button("Send"):
        if user_input.strip():
            # Add user message to conversation history
            st.session_state["conversation"].append({"role": "user", "content": user_input})

            # Send the conversation to GPT for a response
            try:
                with st.spinner("Euripides is thinking..."):
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are Euripides, a conversational assistant helping users explore their identity and passions to create a personal brand."},
                            *st.session_state["conversation"],  # Include the full conversation
                        ]
                    )
                    gpt_reply = response["choices"][0]["message"]["content"]

                # Add GPT response to conversation history
                st.session_state["conversation"].append({"role": "assistant", "content": gpt_reply})

                # Transition to Insights if GPT indicates readiness
                if "ready for insights" in gpt_reply.lower():
                    st.session_state["current_section"] = "insights"
                    st.experimental_rerun()
            except openai.error.AuthenticationError as e:
                st.error("Authentication Error: Please check your API key.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

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
elif st.session_state["current_section"] == "chat":
    chat_interface()
elif st.session_state["current_section"] == "insights":
    insights_section()
