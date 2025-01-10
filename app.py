import streamlit as st
import openai

# --- Configure OpenAI API Key ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Euripides, a GPT-driven assistant designed to help users explore their identity, "
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
    st.session_state.user_profile = {}  # Store gathered user information

# --- Exploration Questions for Each Section ---
questions = {
    "identity": [
        "How do you perceive yourself, and how do you think others perceive you?",
        "What are some of your core beliefs or values that shape how you view the world?",
    ],
    "passions": [
        "What activities or hobbies do you enjoy in your free time?",
        "Are there any guilty pleasures or secret passions you have?",
    ],
    "professional": [
        "What is your current or most recent job? What skills does it involve?",
        "Are there specific skills or strengths you want to highlight in your personal brand?",
    ],
    "dreams": [
        "What is your ultimate goal or dream in life?",
        "What kind of impact would you like to have on the world?",
    ],
    "authenticity": [
        "Are there lived experiences or challenges you’ve faced that shape your story?",
        "What feels authentic for you to share with others?",
    ],
    "audience": [
        "Who do you want to connect with or serve through your digital presence?",
        "Are there communities you’re already part of or want to engage with more deeply?",
    ],
    "time": [
        "How much time do you have to dedicate to creating content or engaging online?",
        "Do you prefer creating text, video, or graphic content?",
    ],
    "leadership": [
        "What areas do you feel most confident or naturally take charge in?",
        "Are there areas where you feel you need more support or guidance?"
    ],
}

# --- Section Handling Function ---
def handle_section():
    section = st.session_state.current_section
    if section == "welcome":
        st.title("Welcome to Euripides!")
        st.subheader("Your personal Deus Ex Machina for crafting your digital presence.")
        st.markdown("Euripides will guide you through an exploration of your identity, passions, and goals.")
        
        user_name = st.text_input("What should I call you?", placeholder="Enter your name")
        reason = st.selectbox(
            "What brings you here today?",
            ["Explore who I am", "Build my digital presence", "Discover my audience", "Other"]
        )
        energy_level = st.slider("How are you feeling right now? (1 = Low energy, 5 = High energy)", 1, 5, 3)

        if st.button("Start Talking to Euripides"):
            st.session_state.user_profile["name"] = user_name
            st.session_state.user_profile["reason"] = reason
            st.session_state.user_profile["energy_level"] = energy_level
            st.session_state.current_section = "identity"  # Move to the next section
            st.experimental_rerun()
    else:
        # Display current section questions
        st.subheader(f"Let's talk about {section.capitalize()}")
        for question in questions.get(section, []):
            st.write(question)
            user_response = st.text_input(f"Your response to: {question}", key=f"{section}_{question}")
            if user_response:
                st.session_state.user_profile.setdefault(section, []).append(user_response)
        
        if st.button("Next Section"):
            # Move to the next section
            sections = list(questions.keys())
            current_index = sections.index(section)
            if current_index + 1 < len(sections):
                st.session_state.current_section = sections[current_index + 1]
            else:
                st.session_state.current_section = "insights"  # Move to insights after exploration
            st.experimental_rerun()

# --- Insights Generation Function ---
def generate_insights():
    st.title("Euripides Insights")
    st.markdown("Here’s what I’ve learned about you and some tailored recommendations:")
    
    # Compile the user profile into a summary for the GPT
    user_summary = "\n".join([f"{key.capitalize()}: {value}" for key, value in st.session_state.user_profile.items()])
    
    with st.spinner("Generating insights..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant summarizing insights."},
                    {"role": "user", "content": user_summary},
                ],
                temperature=0.7,
                max_tokens=500
            )
            insights = response.choices[0].message["content"]
            st.success("Here are your insights:")
            st.write(insights)
        except Exception as e:
            st.error(f"An error occurred while generating insights: {e}")

# --- Main App Logic ---
if st.session_state.current_section == "insights":
    generate_insights()
else:
    handle_section()
