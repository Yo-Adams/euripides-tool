import streamlit as st
import openai

# --- Configure OpenAI API Key ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Welcome Section ---
st.title("Welcome to Euripides!")
st.subheader("Your personal Deus Ex Machina for crafting your digital presence.")

st.markdown("""
Euripides is here to help you explore who you are and craft actionable insights for building your digital presence. Let's get started!
""")

# Collect user's preferred name
user_name = st.text_input("What should I call you?", placeholder="Enter your name")

# Collect user's goal for using the tool
user_goal = st.radio(
    "What brings you here today?",
    options=["Explore who I am", "Build my digital presence", "Discover my audience", "Other"],
)

# --- GPT Integration ---
if st.button("Start Conversation"):
    system_prompt = """
    You are Euripides, a conversational assistant designed to help users explore their identity, passions, and professional goals to craft a digital presence.
    Use adaptive questioning and provide actionable insights based on the user's responses. Maintain a supportive tone and ensure the conversation feels natural.
    """
    
    # Initial user message
    user_message = f"My name is {user_name} and my goal is: {user_goal}"

    # Send to OpenAI GPT
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use gpt-3.5-turbo if gpt-4 isn't available
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
    )
    
    # Display GPT response
    gpt_reply = response["choices"][0]["message"]["content"]
    st.write(f"Euripides: {gpt_reply}")
