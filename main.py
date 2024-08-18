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
    st.markdown("<h1 style='text-align: center; color: white;'> ActiMeet</h1>", unsafe_allow_html=True)
    st.image("images/pipline.png", caption="pipline")
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    if st.sidebar.button("Save API Key"):
        update_config(api_key)

    if st.button("Record Audio"):
        audio_path = record_audio()
        if audio_path:
            st.write(f"Audio saved to: {audio_path}")

    if st.button("Transcribe Latest Audio"):
        transcript_path = transcribe_latest_audio()
        if transcript_path:
            st.write(f"Transcript saved to: {transcript_path}")
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