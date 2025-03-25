import streamlit as st
import google.generativeai as genai
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ✨ Set Page Config
st.set_page_config(page_title="MindEase 🧘‍♂️", layout="wide")

# 🌨️ Advanced Black Theme Styling
black_theme = """
    <style>
    body {
        background: #000000;
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background: transparent;
    }
    .css-18e3th9, .stTextInput, .stButton, .stSelectbox, .stTextArea {
        background: rgba(20, 20, 20, 0.95);
        color: #ffffff;
        border-radius: 20px;
        border: 2px solid #8a2be2;
        padding: 14px;
        transition: all 0.4s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #8a2be2, #4b0082);
        color: white;
        transform: scale(1.05);
    }
    .stChatMessage {
        background: rgba(40, 40, 40, 0.9);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.5);
    }
    .sidebar .css-1d391kg {
        background: linear-gradient(135deg, #8a2be2, #4b0082);
        color: white;
    }
    .title {
        text-align: center;
        font-size: 4em;
        font-weight: 900;
        color: #8a2be2;
        text-shadow: 3px 3px 12px #4b0082;
        margin-bottom: 40px;
    }
    .subheading {
        font-size: 1.5em;
        color: #b39ddb;
        text-align: center;
    }
    </style>
"""
st.markdown(black_theme, unsafe_allow_html=True)

# ✨ Configure API Key
genai.configure(api_key="AIzaSyBj1BzzNCg6FOUeic8DTtU3uYNVMaDErQw")

# 📌 Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'moods' not in st.session_state:
    st.session_state.moods = []
if 'journals' not in st.session_state:
    st.session_state.journals = []

# 🤖 Chatbot Function
def get_gemini_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)
    return response.text

# 📊 Mood Tracker
def log_mood(mood):
    today = datetime.date.today().strftime("%Y-%m-%d")
    st.session_state.moods.append({"date": today, "mood": mood})

def show_mood_chart():
    if st.session_state.moods:
        df = pd.DataFrame(st.session_state.moods)
        mood_counts = df["mood"].value_counts()
        fig, ax = plt.subplots()
        mood_counts.plot(kind='bar', ax=ax, color=['#8a2be2', '#4CAF50', '#FF6347', '#4682B4', '#FFA500'])
        ax.set_title("Mood Analytics")
        ax.set_xlabel("Mood")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

def export_csv(data, filename):
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, filename, "text/csv", key=filename)

# ✨ Sidebar Navigation
st.sidebar.title("MindEase 🧘‍♂️")
page = st.sidebar.radio("Navigate", ["Chatbot", "Mood Tracker", "Journal", "Meditation Music", "Breathing Exercise", "Affirmations", "Help & Resources"])

# 🤖 Chatbot UI
if page == "Chatbot":
    st.markdown("<div class='title'>Mental Health Chatbot 🤖</div>", unsafe_allow_html=True)

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["text"])

    user_input = st.chat_input("How are you feeling today?")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        response = get_gemini_response(user_input)
        st.session_state.chat_history.append({"role": "ai", "text": response})
        st.rerun()

# 📊 Mood Tracker
elif page == "Mood Tracker":
    st.markdown("<div class='title'>Mood Tracker 📊</div>", unsafe_allow_html=True)
    mood = st.selectbox("How do you feel today?", ["Happy", "Sad", "Anxious", "Angry", "Calm", "Stressed", "Relaxed"])
    if st.button("Log Mood"):
        log_mood(mood)
        st.success("Mood Logged Successfully!")
    show_mood_chart()
    if st.session_state.moods:
        export_csv(st.session_state.moods, "mood_log.csv")

# 📚 Daily Journal
elif page == "Journal":
    st.markdown("<div class='title'>Daily Journal 📚</div>", unsafe_allow_html=True)
    entry = st.text_area("Write your thoughts here:")
    if st.button("Save Journal"):
        today = datetime.date.today().strftime("%Y-%m-%d")
        st.session_state.journals.append({"date": today, "entry": entry})
        st.success("Journal entry saved!")

    st.write("### Past Entries")
    for journal in reversed(st.session_state.journals):
        st.write(f"**{journal['date']}**: {journal['entry']}")

    if st.session_state.journals:
        export_csv(st.session_state.journals, "journal_log.csv")

# 🎵 Meditation Music
elif page == "Meditation Music":
    st.markdown("<div class='title'>Meditation Music 🎵</div>", unsafe_allow_html=True)
    st.audio("https://www.bensound.com/bensound-music/bensound-relaxing.mp3")

# 🌬️ Breathing Exercise
elif page == "Breathing Exercise":
    st.markdown("<div class='title'>Breathing Exercise 🌬️</div>", unsafe_allow_html=True)
    st.write("Follow the guided breathing pattern:")
    st.write("Inhale deeply...")
    st.progress(33)
    st.write("Hold your breath...")
    st.progress(66)
    st.write("Exhale slowly...")
    st.progress(100)

# ✨ Daily Affirmations
elif page == "Affirmations":
    st.markdown("<div class='title'>Daily Affirmations ✨</div>", unsafe_allow_html=True)
    affirmations = ["You are strong and capable.", "Every day is a new opportunity."]
    st.write(f"**{affirmations[datetime.datetime.now().day % len(affirmations)]}**")

# 📖 Help & Resources
elif page == "Help & Resources":
    st.markdown("<div class='title'>Help & Resources 📖</div>", unsafe_allow_html=True)
    st.write("### Mental Health Resources")
    st.write("- [National Alliance on Mental Illness (NAMI)](https://www.nami.org)")
    st.write("- [MentalHealth.gov](https://www.mentalhealth.gov)")
    st.write("- [Crisis Text Line](https://www.crisistextline.org)")