import openai 
import streamlit as st
from record_audio import record_audio
from transcriber import transcribe_latest_audio
from show_tasks import display_summary
import subprocess
import concurrent.futures
import json 
import os

def run_script(script_name):
    """Run a script and return the output."""
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    return result.stdout, result.stderr

def main():
    # Initialize the summarizer_extractor_running state
    if 'summarizer_extractor_running' not in st.session_state:
        st.session_state.summarizer_extractor_running = False

    # Contact Section
    st.markdown("<h2 style='text-align: center; color: white;'>Contact</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("[Abdullah Alhabib](https://www.linkedin.com/in/abdullah-alhabib20?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app)", unsafe_allow_html=True)

    with col2:
        st.markdown("[Fahad Alotaibi](https://www.linkedin.com/in/fahad-f-alotaibi/)", unsafe_allow_html=True)

    with col3:
        st.markdown("[Abdullah Alwhaibi](https://www.linkedin.com/in/abdullah-alwehaibi-b880901ab/)", unsafe_allow_html=True)

    with col4:
        st.markdown("[Abdulrahman Algamdi](https://www.linkedin.com/in/abdulrahman-alghamdi-732283287/)", unsafe_allow_html=True)

    st.image("images/icon_1.webp", width=100)

    st.markdown("<h2 style='text-align: center; color: white;'>The Meeting Wizard</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>Unlock the Power of In-person Meeting Using LLM + LAM Capabilities</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.expander("Overview"):
            st.write("""
This project develops an AI system to streamline meetings by automating transcription, summarization, and task management, seamlessly integrating with existing tools to enhance efficiency and productivity.
            """)

    with col2:
        with st.expander("Pipeline"):
            st.image("images/pip.png", caption="Pipeline")

    with col3:
        with st.expander("Technologies"):
            st.image("images/tech.png", caption="Technologies")

    with col4:
        with st.expander("Future Work"):
            st.image("images/future_work.png", caption="Future Work")

    audio_path = record_audio()
    if audio_path:
        st.write(f"Audio saved to: {audio_path}")
        
    st.title("Transcription")

    if st.button("Transcribe Latest Audio"):
        transcript_path = transcribe_latest_audio()
        if transcript_path:
            st.success("Transcription has been saved successfully :)")
            
    st.title("Try meeting wizard now !")
    
    if st.button("Run pipeline"):
        st.session_state.summarizer_extractor_running = True

    if st.session_state.summarizer_extractor_running:
        with st.spinner("Running summarizer and extractor..."):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_summarizer = executor.submit(run_script, 'summarizer.py')
                future_extractor = executor.submit(run_script, 'extractor.py')

                summarizer_output, summarizer_error = future_summarizer.result()
                extractor_output, extractor_error = future_extractor.result()

            if summarizer_error:
                st.error(f"Summarizer error: {summarizer_error}")
            else:
                st.success("Summarizer completed successfully!")
                st.text(summarizer_output)

            if extractor_error:
                st.error(f"Extractor error: {extractor_error}")
            else:
                st.success("Extractor completed successfully!")
                st.text(extractor_output)

            if not summarizer_error and not extractor_error:
                st.session_state.summarizer_extractor_running = True
                display_summary()

if __name__ == "__main__":
    main()