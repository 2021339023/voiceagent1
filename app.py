import streamlit as st
import requests
from io import BytesIO
import time

st.set_page_config(page_title="Multilingual TTS App", layout="centered")
st.title("🌐 Multilingual Text-to-Speech App (ElevenLabs)")

# -----------------------------
# Set your ElevenLabs API Key here
# Or use environment variable / Streamlit Secrets
API_KEY = "YOUR_API_KEY_HERE"  # <-- Replace with your key
# -----------------------------

# Supported languages (informational)
languages = {
    "English": "en",
    "Bengali": "bn",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Mandarin)": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Urdu": "ur",
    "Portuguese": "pt",
    "Russian": "ru",
    "Tamil": "ta",
    "Telugu": "te"
}

# User inputs
text = st.text_area("Enter your text here (can be long):", max_chars=5000)
lang_choice = st.selectbox("Select Language (informational):", list(languages.keys()))
voice_choice = st.selectbox("Select Voice:", ["Rachel", "Antoni", "Bella", "Elli"])

# Function to chunk long text
def chunk_text(text, max_chars=500):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks

if st.button("Convert to Speech"):
    if text.strip() == "":
        st.warning("Please enter some text!")
    else:
        audio_bytes = BytesIO()
        chunks = chunk_text(text, max_chars=500)

        try:
            for idx, chunk in enumerate(chunks):
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_choice}"
                headers = {
                    "xi-api-key": API_KEY,
                    "Content-Type": "application/json"
                }
                payload = {
                    "text": chunk,
                    "voice": voice_choice,
                    "model_id": "eleven_monolingual_v1"
                }

                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    audio_bytes.write(response.content)
                    time.sleep(0.5)  # small delay to avoid rate limit
                else:
                    st.error(f"Failed on chunk {idx+1}: {response.status_code} {response.text}")
                    st.stop()

            audio_bytes.seek(0)
            st.audio(audio_bytes, format="audio/mpeg")

            st.download_button(
                label="Download MP3",
                data=audio_bytes,
                file_name="speech.mp3",
                mime="audio/mpeg"
            )

            st.success("✅ Speech generated successfully!")
        except Exception as e:
            st.error(f"Error generating speech: {e}")
