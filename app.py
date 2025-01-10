import streamlit as st
import openai
import time

# --- OpenAI API Configuration ---
openai.api_key = st.secrets.get("OPENAI_API_KEY")

# --- System Prompt for Euripides ---
SYSTEM_PROMPT = """
You are Euripides, a highly specialized and insightful conversational assistant. Your purpose is to help users explore their identity, passions, and professional goals in a conversational manner to craft actionable insights for their digital presence. 
Your workflow includes three phases: Welcome, Exploration, and Insights. During Exploration, ask adaptive, tailored questions across eight sections: Identity, Passions, Professional Background, Dreams, Authenticity, Audience, Time Use, and Leadership. Save insights for the final phase and focus on gathering detailed user input.
Maintain a supportive and conversational tone. If users provide minimal or hesitant responses, encourage elaboration. Redirect problematic or negative inputs constructively. Always personalize your responses using the user's name.
"""

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""

# --- Typing Effect Function ---
def display_typing_effect(response_text):
    """Simulates typing effect for Euripides' responses."""
    typing_display = ""
    for char in response_text:
        typing_display += char
        time.sleep(0.03)  # Simulate typing speed
        st.markdown(
            f"""
            <div style="background-color: #f0f4c3; padding: 10px; margin: 5px; border-radius: 10px; text-align: left; max-width: 70%; float: right;">
                <b>Euripides is typing...</b><br>{typing_display}
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- App Title and Introduction ---
st.title("Euripides: Your Personal Deus Ex Machina")
st.subheader("Let's explore who you are and craft actionable insights for your digital presence!")

# --- Welcome Phase ---
if not st.session_state["user_name"]:
    st.markdown("**Welcome to Euripides! Let's start by getting to know you.**")
    st.session_state["user_name"] = st.text_input("What should I call you?")
    user_goal = st.selectbox(
        "Why are you here today?",
        [
            "Explore who I am",
            "Build my digital presence",
            "Discover my audience",
            "Other",
        ],
    )
    energy_level = st.slider(
        "How much energy do you have for this conversation?",
        min_value=1,
        max_value=10,
        value=7,
    )

    if st.button("Start Talking to Euripides"):
        # Store initial user data in session state
        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": f"Great to meet you, {st.session_state['user_name']}! You want to {user_goal.lower()} and have an energy level of {energy_level}/10. Let's begin!",
            }
        )
        st.experimental_rerun()

# --- Chat Interface ---
st.subheader(f"Chat with Euripides, {st.session_state['user_name']}")

# User Input
user_input = st.text_area(
    "You:", placeholder="Type your message here...", height=50, key="chat_input"
)

if st.button("Send", key="send_button"):
    if user_input.strip():  # Check if input is not empty
        # Add user input to session state
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Call OpenAI API
        with st.spinner("Euripides is thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=st.session_state["messages"],
                temperature=0.7,
                max_tokens=150,
            )

        # Get assistant's reply
        assistant_reply = response["choices"][0]["message"]["content"]

        # Save assistant's reply
        st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})

        # Display assistant reply
        display_typing_effect(assistant_reply)

# --- Display Conversation History ---
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"""
        <div style="background-color: #e8f5e9; padding: 10px; margin: 5px; border-radius: 10px; text-align: left; max-width: 70%;">
            <b>You:</b> {message['content']}
        </div>
        """, unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"""
        <div style="background-color: #f0f4c3; padding: 10px; margin: 5px; border-radius: 10px; text-align: left; max-width: 70%; float: right;">
            <b>Euripides:</b> {message['content']}
        </div>
        """, unsafe_allow_html=True)
