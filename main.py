import streamlit as st
from record_audio import record_audio
from  transcriber import transcribe_latest_audio
from show_tasks import display_summary
import subprocess
import concurrent.futures
import json 
import os

def update_config(api_key):
    config_path = 'config.json'
    # Load existing config or create a new one
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    # Update the API key
    config["openai_api_key"] = api_key

    # Save the updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    st.success("API key saved successfully!")

def run_script(script_name):
    """Run a script and return the output."""
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    return result.stdout, result.stderr

def main():
    with st.container():
        cols = st.columns(1)
        with cols[0]:
            st.image("images/icon_1.webp", width=100)



    # Center the subtitle
    st.markdown("<h2 style='text-align: center; color: white;'>The Meeting Wizard</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'> Unlock the Power of In-person Meeting Using LLM + LAM Capabilities</h3>", unsafe_allow_html=True)

    # Create four columns with expander taps
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.expander("Overview"):
            st.write(f"""

This project develops an AI system to streamline meetings by automating transcription, summarization, and task management, seamlessly integrating with existing tools to enhance efficiency and productivity.                   
                     """)

    with col2:
        with st.expander("Pipeline"):
                st.image("images/pip.png", caption="Pipline")

    with col3:
        with st.expander("Technologies"):
            st.image("images/tech.png", caption="Technologies")

    with col4:
        with st.expander("Future Work"):
            st.image("images/future_work.png", caption="Future Work")

    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    if st.sidebar.button("Save API Key"):
        update_config(api_key)

    audio_path = record_audio()
    if audio_path:
            st.write(f"Audio saved to: {audio_path}")
    st.title("Transcription")

    if st.button("Transcribe Latest Audio"):
        transcript_path = transcribe_latest_audio()
        if transcript_path:
            st.success(f"Transcribtion has been saved successfully :)")    
    if st.button("Run Summarizer and Extractor"):
        with st.spinner("Running summarizer and extractor..."):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future_summarizer = executor.submit(run_script, 'summarizer.py')
                    future_extractor = executor.submit(run_script, 'extractor.py')

                    # Collect the results
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

                # If both scripts run successfully, run show_task.py
                if not summarizer_error and not extractor_error:
                    st.success("Both scripts completed successfully. Running show_task.py...")
                    display_summary()
                    # show_task_output, show_task_error = run_script('show_tasks.py')
                    # if show_task_error:
                    #     st.error(f"Show Task error: {show_task_error}")
                    # else:
                    #     st.success("Show Task completed successfully!")
                    #     st.text(show_task_output)

if __name__ == "__main__":
    main()