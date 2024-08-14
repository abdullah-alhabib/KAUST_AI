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

    # Transcribe audio
    result = model.transcribe(latest_audio)

    # Get the filename without extension
    audio_filename = os.path.splitext(os.path.basename(latest_audio))[0]

    # Create transcript filename
    transcript_filename = f"transcript_{audio_filename}.txt"
    transcript_path = os.path.join("transcript", transcript_filename)

    # Save transcript
    with open(transcript_path, "w") as f:
        f.write(result["text"])

    st.write(f"Transcription saved to: {transcript_path}")
    st.write("Transcript:")
    st.write(result["text"])

    return transcript_path