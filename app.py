import streamlit as st
import pyttsx3
from io import BytesIO
import tempfile

st.set_page_config(page_title="Offline TTS App", layout="centered")
st.title("🌐 Offline Multilingual Text-to-Speech (pyttsx3)")

# List available voices
engine = pyttsx3.init()
voices = engine.getProperty('voices')
voice_names = [v.name for v in voices]

text = st.text_area("Enter your text here (any length):", max_chars=10000)
voice_choice = st.selectbox("Select Voice:", voice_names)

if st.button("Convert to Speech"):
    if not text.strip():
        st.warning("Please enter some text!")
    else:
        try:
            # Temporary file to save mp3
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                engine.setProperty('voice', voices[voice_names.index(voice_choice)].id)
                engine.save_to_file(text, f.name)
                engine.runAndWait()
                f.seek(0)
                audio_bytes = f.read()

            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                label="Download MP3",
                data=audio_bytes,
                file_name="speech.mp3",
                mime="audio/mpeg"
            )

            st.success("✅ Speech generated successfully (offline)!")
        except Exception as e:
            st.error(f"Error generating speech: {e}")
