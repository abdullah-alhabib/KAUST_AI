import os
import glob
import whisper
import streamlit as st

def transcribe_latest_audio():

    # Create the 'transcript' directory if it doesn't exist
    os.makedirs("transcript", exist_ok=True)

    # Find the latest audio file
    list_of_files = glob.glob('audio/*.wav')
    if not list_of_files:
        st.write("No audio files found in the 'audio' directory.")
        return None

    latest_audio = max(list_of_files, key=os.path.getctime)
    
    # Load Whisper model
    model = whisper.load_model("base")

    # Transcribe audio with language detection
    result = model.transcribe(latest_audio, language=None)  # language=None allows auto-detection

    # Detect the language
    detected_language = result["language"]

    # Get the filename without extension
    audio_filename = os.path.splitext(os.path.basename(latest_audio))[0]

    # Create transcript filename
    transcript_filename = f"transcript_{audio_filename}.txt"
    transcript_path = os.path.join("transcript", transcript_filename)

    # Save transcript with UTF-8 encoding
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(f"Detected language: {detected_language}\n")
        f.write(result["text"])

    # Display the results in Streamlit
    col1, col2, = st.columns(2)

    with col1:
        with st.expander("Detected language"):
            st.write(f"Detected language: {detected_language}")
    with col2:
        with st.expander("Transcript"):
            st.write(f"Transcript:: {result["text"]}")

    return transcript_path
