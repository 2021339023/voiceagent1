import streamlit as st
from gtts import gTTS
from io import BytesIO
import time

st.set_page_config(page_title="Multilingual TTS App", layout="centered")
st.title("🌐 Multilingual Text-to-Speech (Free gTTS)")

# Supported languages
languages = {
    "English": "en",
    "Bengali": "bn",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Urdu": "ur",
    "Portuguese": "pt",
    "Russian": "ru",
    "Tamil": "ta",
    "Telugu": "te"
}

# User input
text = st.text_area("Enter your text here (max 5000 chars):", max_chars=5000)
lang_choice = st.selectbox("Select Language:", list(languages.keys()))

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
    if not text.strip():
        st.warning("Please enter some text!")
    else:
        audio_bytes = BytesIO()
        chunks = chunk_text(text, max_chars=500)
        
        try:
            for idx, chunk in enumerate(chunks):
                tts = gTTS(text=chunk, lang=languages[lang_choice])
                tts.write_to_fp(audio_bytes)
                time.sleep(1)  # small delay to reduce 429 errors

            audio_bytes.seek(0)
            
            # Play audio
            st.audio(audio_bytes, format="audio/mp3")

            # Download button
            st.download_button(
                label="Download MP3",
                data=audio_bytes,
                file_name="speech.mp3",
                mime="audio/mpeg"
            )

            st.success(f"✅ Speech generated in {lang_choice}!")
        except Exception as e:
            st.error(f"Error generating speech: {e}\nTry smaller text or wait a few seconds before retrying.")
