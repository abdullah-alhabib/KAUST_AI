import streamlit as st
from audiorecorder import audiorecorder
from datetime import datetime
import os


def record_audio():
    st.title("Audio Recorder")
    audio = audiorecorder("Click to record!", "Click to stop recording",)

    if len(audio) > 0:
        # Play the recorded audio in the frontend
        st.audio(audio.export().read())

        # Create the 'audio' directory if it doesn't exist
        os.makedirs("audio", exist_ok=True)

        # Generate a unique filename using a timestamp,
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file_path = os.path.join("audio", f"audio_{timestamp}.wav")

        # Save the audio file
        audio.export(audio_file_path, format="wav")

        # Display success message indicating the file has been saved
        st.success(f"Audio has been recorded and saved successfully :)")

        # Display additional audio properties
        #st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

        return audio_file_path

    return None
