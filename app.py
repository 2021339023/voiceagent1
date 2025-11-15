import streamlit as st
import requests
from io import BytesIO
import os

st.title("Multilingual Text-to-Voice App (Stable TTS)")

# ElevenLabs API Key (set in environment or hardcode here)
API_KEY = os.getenv("ELEVENLABS_API_KEY", "YOUR_API_KEY_HERE")  # Replace YOUR_API_KEY_HERE

# User input
text = st.text_area("Enter your text here (max 1000 chars):", max_chars=1000)
voice_choice = st.selectbox("Select Voice:", ["Rachel", "Antoni", "Bella", "Elli"])

if st.button("Convert to Speech"):
    if text:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_choice}"
        headers = {
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "voice": voice_choice,
            "model_id": "eleven_monolingual_v1"
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                audio_bytes = BytesIO(response.content)
                audio_bytes.seek(0)

                # Play audio in browser
                st.audio(audio_bytes, format="audio/mpeg")

                # Download button
                st.download_button(
                    label="Download MP3",
                    data=audio_bytes,
                    file_name="speech.mp3",
                    mime="audio/mpeg"
                )

                st.success("Speech generated successfully!")
            else:
                st.error(f"Failed to generate speech: {response.status_code} {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some text!")
