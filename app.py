import os
import io
import streamlit as st
import google.generativeai as genai
from models.resume_parser import extract_resume_text, extract_entities
from models.speech_processing import text_to_speech
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av

import asyncio
import sys

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# --- Configure Gemini API Key ---
genai.configure(api_key="AIzaSyBUF9Kyu2NvWrJ1VII2uOE-QgEYBe7AZ4M")

st.title("🤖 AI Interview Chatbot")

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_buffer = bytes()
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        pcm = frame.to_ndarray()
        self.audio_buffer += pcm.tobytes()
        return frame

def process_audio(audio_bytes):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(io.BytesIO(audio_bytes))
    with audio_file as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError:
        return "Error connecting to recognition service."

job_description = st.text_area("📝 Paste Job Description Here:")

if job_description:
    st.write("✅ Job Description Received!")
    
    uploaded_resume = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])
    if uploaded_resume:
        if not os.path.exists("data"):
            os.makedirs("data")
        with open("data/uploaded_resume.pdf", "wb") as f:
            f.write(uploaded_resume.read())
        resume_text = extract_resume_text("data/uploaded_resume.pdf")
        candidate_info = extract_entities(resume_text)
        st.write("✅ Resume Parsed Successfully!")
        st.write("Candidate Info:", candidate_info)
    
    st.write("💬 AI Interview Chatbot is ready to talk!")
    
    for entry in st.session_state.conversation_history:
        st.write(f"**{entry['role']}:** {entry['content']}")
    
    input_method = st.radio("Select Input Method", ("Text"), index=0)
    
    if input_method == "Text":
        user_response = st.text_input("🎤 Type your answer:", key="text_input")
        if st.button("Send Answer (Text)"):
            if not user_response:
                st.warning("⚠️ Please provide an answer!")
            else:
                st.session_state.conversation_history.append({"role": "Candidate", "content": user_response})
                
                model = genai.GenerativeModel("gemini-2.0-flash")
                prompt = (
                    f"You are a friendly and engaging interviewer for a {job_description} position. "
                    f"The candidate just said: '{user_response}'. Ask a follow-up question in a natural conversational tone."
                )
                response = model.generate_content(prompt)
                bot_reply = response.text
                st.session_state.conversation_history.append({"role": "Interviewer", "content": bot_reply})
                st.write(f"**Interviewer:** {bot_reply}")
                text_to_speech(bot_reply)

        
       
    
    if st.button("End Interview"):
        final_advice = (
            "Final advice: Based on your responses, consider elaborating more on your technical challenges "
            "and achievements. Reflect on how you handled difficulties and think about how to present your experience more confidently."
        )
        st.write("### Final Advice and Corrections")
        st.write(final_advice)
        text_to_speech(final_advice)
