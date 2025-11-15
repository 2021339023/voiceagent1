import streamlit as st
from gtts import gTTS
from io import BytesIO

st.title("Multilingual Text-to-Voice App")

# gTTS supported languages
languages = {
    "Afrikaans": "af",
    "Arabic": "ar",
    "Bengali": "bn",
    "Chinese (Mandarin)": "zh-cn",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Finnish": "fi",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Korean": "ko",
    "Latin": "la",
    "Malay": "ms",
    "Marathi": "mr",
    "Norwegian": "no",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Welsh": "cy"
}

# User input
text = st.text_area("Enter your text here (max 1000 chars):", max_chars=1000)
lang_choice = st.selectbox("Select Language:", list(languages.keys()))

if st.button("Convert to Speech"):
    if text:
        try:
            # Generate speech
            tts = gTTS(text=text, lang=languages[lang_choice])
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
        except Exception as e:
            st.error(f"Error generating speech: {e}\nPlease try again.")
            st.stop()  # Stop further execution if error occurs

        # Play audio in browser
        st.audio(audio_bytes, format='audio/mp3')
        st.success(f"Speech generated in {lang_choice}!")

        # Download button
        st.download_button(
            label="Download MP3",
            data=audio_bytes,
            file_name="speech.mp3",
            mime="audio/mpeg"
        )
    else:
        st.warning("Please enter some text!")
