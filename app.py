import streamlit as st

# App Title and Introduction
st.title("Welcome to Euripides!")
st.subheader("Your personal Deus Ex Machina for crafting your digital presence.")

# Welcome Section
st.markdown("""
    Euripides is here to help you explore who you are and how you can build a digital presence that reflects your unique persona. Let's start by getting to know you.
""")

# Ask for the user's preferred name
user_name = st.text_input("What should I call you?", placeholder="Enter your name")

# Ask for the user's goals
user_goal = st.radio(
    "What brings you here today?",
    options=["Explore who I am", "Build my digital presence", "Discover my audience", "Other"],
)

# Initial energy check-in
energy_level = st.slider(
    "How much energy do you have for this conversation today? (1 = Low, 10 = High)", 
    1, 10, 5
)

# Display feedback based on energy level
if energy_level <= 3:
    st.warning(f"Take it slow today, {user_name or 'friend'}. We'll keep it simple!")
elif energy_level >= 7:
    st.success(f"Great energy, {user_name or 'friend'}! Let's dive in!")

# Navigation to the next section
if st.button("Start Exploring"):
    st.write(f"Alright, {user_name or 'friend'}, let's start exploring your persona!")
    # Placeholder for Exploration Section
    st.write("Coming soon: Exploration Section!")

