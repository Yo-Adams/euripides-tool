import streamlit as st
import openai
import time

# Configure API Key
openai.api_key = st.secrets.get("OPENAI_API_KEY")

# System Prompt
SYSTEM_PROMPT = """
You are Euripides, a highly specialized conversational assistant...
"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]

# Define typing effect
def display_typing_effect(response_text):
    typing_display = ""
    for char in response_text:
        typing_display += char
        st.markdown(f"""
        <div style="background-color: #f0f4c3; padding: 10px; margin: 5px; border-radius: 10px; text-align: left; max-width: 70%; float: right;">
            <b>Euripides is typing...</b><br>{typing_display}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.03)

# Chat interface
st.title("Euripides: Your Personal Deus Ex Machina")
st.subheader("Chat with Euripides")

user_input = st.text_area("You:", placeholder="Type your message here...", height=50)
if st.button("Send"):
    if user_input:
        # Add user input to session
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # API Call
        with st.spinner("Euripides is thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=st.session_state["messages"],
                temperature=0.7,
                max_tokens=150,
            )

        # Get assistant's reply
        assistant_reply = response["choices"][0]["message"]["content"]

        # Simulate typing effect
        display_typing_effect(assistant_reply)

        # Save assistant's reply
        st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})

# Display conversation
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**Euripides:** {message['content']}")
