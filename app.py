import streamlit as st
from gtts import gTTS
from io import BytesIO

# --- Configuration ---
st.set_page_config(
    page_title="Multilingual Text-to-Voice App",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("🗣️ Multilingual Text-to-Voice App")
st.markdown("Convert text into speech using the Google Translate TTS engine.")

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

# --- Core Conversion Function ---

def convert_text_to_speech(text, lang_code):
    """Generates MP3 audio from text using gTTS."""
    try:
        # Generate speech
        tts = gTTS(text=text, lang=lang_code)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        # Check specifically for the 429 error which indicates rate limiting
        if "429 (Too Many Requests)" in str(e):
            st.error(
                "🚨 **Rate Limit Error (429: Too Many Requests)**"
                "\n\nIt seems the server has reached its temporary limit for text-to-speech requests. "
                "Please wait a few minutes (e.g., 15-30 minutes) and try again."
                "\n\nFor high-volume or production use, consider switching to the official Google Cloud Text-to-Speech API."
            )
        else:
            st.error(f"❌ An unknown error occurred: {e}")
            st.warning("Please check your text and language selection and try again.")
        return None

# --- Streamlit UI ---

# User input
text = st.text_area(
    "📝 Enter your text here (max 1000 chars):", 
    max_chars=1000,
    height=150
)

# Sidebar for language selection (better use of screen space)
with st.sidebar:
    st.header("⚙️ Settings")
    lang_choice = st.selectbox(
        "Select Language:", 
        list(languages.keys()),
        index=languages.get('en', 0) # Default to English
    )
    st.info("The accuracy of the voice depends on the chosen language and its availability in the gTTS library.")

if st.button("🎙️ Convert to Speech", use_container_width=True):
    if not text:
        st.warning("⚠️ Please enter some text before converting!")
    else:
        # Get the language code
        lang_code = languages[lang_choice]
        
        # Convert and handle output
        audio_data = convert_text_to_speech(text, lang_code)
        
        if audio_data:
            st.success(f"✅ Speech successfully generated in **{lang_choice}**!")
            
            # Use columns to align the audio player and download button
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.audio(audio_data, format='audio/mp3', start_time=0)
            
            with col2:
                # Need to seek to 0 again for the download button to work correctly
                audio_data.seek(0) 
                st.download_button(
                    label="⬇️ Download MP3",
                    data=audio_data,
                    file_name=f"speech_{lang_code}.mp3",
                    mime="audio/mpeg",
                    key="download_button"
                )
