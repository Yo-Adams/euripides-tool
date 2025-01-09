import streamlit as st
import openai

# --- OpenAI API Key Configuration ---
# Ensure your API key is stored securely in Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Euripides, a conversational assistant designed to help users explore their identity, passions, and professional goals to craft actionable insights for their digital presence."}
    ]

# --- Chat Interface Function ---
def chat_interface():
    st.title("Euripides")
    st.subheader("Your personal Deus Ex Machina for crafting your digital presence")
    
    # Introduction text
    st.markdown("""
    **Euripides** is here to help you explore who you are, identify your passions, and craft actionable insights for your digital presence. Let's get started!
    """)

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        elif message["role"] == "assistant":
            st.chat_message("assistant").markdown(message["content"])

    # User input
    if user_input := st.chat_input("Type your message here..."):
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate assistant response
        with st.spinner("Euripides is thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Replace with "gpt-3.5-turbo" if GPT-4 is not available
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=500
                )
                assistant_message = response.choices[0].message["content"]
            except Exception as e:
                assistant_message = f"An error occurred: {e}"

        # Add assistant message to session state
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

# --- Run the Chat Interface ---
if __name__ == "__main__":
    chat_interface()

