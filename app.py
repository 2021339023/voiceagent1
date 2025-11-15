import streamlit as st
from gtts import gTTS
from io import BytesIO
import time

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

text = st.text_area("Enter your text (max 1000 chars):", max_chars=1000)
lang_choice = st.selectbox("Select Language:", list(languages.keys()))

if st.button("Convert to Speech"):
    if not text.strip():
        st.warning("Please enter some text!")
    else:
        try:
            tts = gTTS(text=text, lang=languages[lang_choice])
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format="audio/mp3")
            
            st.download_button(
                label="Download MP3",
                data=audio_bytes,
                file_name="speech.mp3",
                mime="audio/mpeg"
            )
            st.success(f"Speech generated in {lang_choice}!")
        except Exception as e:
            st.error(f"Error generating speech: {e}\nTry smaller text or wait a few seconds before retrying.")
