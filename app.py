import streamlit as st
import openai

# --- Configure OpenAI API Key ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Euripides, a conversational assistant designed to help users explore their identity, "
            "passions, and professional goals. Guide the user through structured sections, collecting "
            "information about their identity, passions, professional background, dreams, authenticity, "
            "audience alignment, time use, and leadership. Focus on gathering and clarifying user responses. "
            "Do not provide insights or recommendations during the exploration phase. After sufficient "
            "information is collected, provide a tailored summary, insights, and actionable steps."
        )}
    ]
if "current_section" not in st.session_state:
    st.session_state.current_section = "welcome"  # Start with the welcome section
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

# --- Function to Handle Chat Messages ---
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- Generate GPT Response ---
def get_gpt_response():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"An error occurred: {e}"

# --- Chat Interface ---
st.title("Welcome to Euripides!")
st.markdown("Your personal Deus Ex Machina for crafting your digital presence.")

if st.session_state.current_section == "welcome":
    # Welcome Screen
    if "welcome_shown" not in st.session_state:
        add_message("assistant", "Welcome! What should I call you?")
        st.session_state.welcome_shown = True

    user_input = st.chat_input("Type your response here...")
    if user_input:
        add_message("user", user_input)
        if "name" not in st.session_state.user_profile:
            st.session_state.user_profile["name"] = user_input
            add_message("assistant", f"Nice to meet you, {user_input}! What brings you here today?")
        elif "reason" not in st.session_state.user_profile:
            st.session_state.user_profile["reason"] = user_input
            add_message("assistant", "Great! Before we dive in, how are you feeling on a scale of 1 (low energy) to 5 (high energy)?")
        elif "energy_level" not in st.session_state.user_profile:
            try:
                energy = int(user_input)
                if 1 <= energy <= 5:
                    st.session_state.user_profile["energy_level"] = energy
                    add_message("assistant", "Thanks! Let's get started. I'll guide you through some questions.")
                    st.session_state.current_section = "identity"
                else:
                    add_message("assistant", "Please provide a number between 1 and 5.")
            except ValueError:
                add_message("assistant", "Please provide a valid number between 1 and 5.")

elif st.session_state.current_section in ["identity", "passions", "professional", "dreams", "authenticity", "audience", "time", "leadership"]:
    # Exploration Sections
    questions = {
        "identity": ["How do you perceive yourself?", "How do others perceive you?"],
        "passions": ["What are your hobbies or interests?", "Do you have any secret passions?"],
        "professional": ["What is your current or most recent job?", "What skills do you want to highlight?"],
        "dreams": ["What is your ultimate goal?", "What impact do you want to have?"],
        "authenticity": ["What lived experiences shape your story?", "What feels authentic for you to share?"],
        "audience": ["Who do you want to connect with?", "Are there communities you're already part of?"],
        "time": ["How much time do you have for creating content?", "Do you prefer creating text, video, or graphics?"],
        "leadership": ["What areas do you feel most confident in?", "Where do you need more support?"],
    }

    section = st.session_state.current_section
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0

    current_questions = questions[section]
    if st.session_state.question_index < len(current_questions):
        current_question = current_questions[st.session_state.question_index]
        add_message("assistant", current_question)
        user_input = st.chat_input("Type your response here...")
        if user_input:
            add_message("user", user_input)
            st.session_state.user_profile.setdefault(section, []).append(user_input)
            st.session_state.question_index += 1
    else:
        # Move to the next section
        st.session_state.question_index = 0
        sections = list(questions.keys())
        current_index = sections.index(section)
        if current_index + 1 < len(sections):
            st.session_state.current_section = sections[current_index + 1]
            add_message("assistant", f"Let's move on to {sections[current_index + 1].capitalize()}.")
        else:
            st.session_state.current_section = "insights"
            add_message("assistant", "Thanks for sharing! Let's review what we've learned.")

elif st.session_state.current_section == "insights":
    # Insights Section
    add_message("assistant", "Generating insights based on what you've shared...")
    user_summary = "\n".join([f"{key.capitalize()}: {value}" for key, value in st.session_state.user_profile.items()])
    insights = get_gpt_response()
    add_message("assistant", insights)

# Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
