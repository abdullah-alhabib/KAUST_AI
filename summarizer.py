import openai
import json  # for reading JSON config
import os  # for creating directories
import re   
import streamlit as st
# Load configuration
def load_config(config_file):
    if config_file.endswith('.json'):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported configuration file format. Please use JSON or YAML.")

# Initialize configuration
config = load_config('config.json')  # Change to 'config.yaml' if you're using YAML

# Set API key and other parameters
openai.api_key = config['openai_api_key']
model = config['model']
temperature = config['temperature']
max_tokens = config['max_tokens']
#print(f"model: {model}, temperature: {temperature}, max_tokens: {max_tokens}")

def extract_tasks(transcript):
    # Optimized Prompt for extracting and detailing tasks
    prompt = f"""
    You're an AI specialized in analyzing meeting transcripts. Below is a transcript of a meeting. Your task is to summarize the meeting, focusing on:
    
    brief description of the meeting
    The main points discussed
    Decisions made
    Action items
    The summary should be clear and concise.

    Here is the transcript:
    "{transcript}"

    Please return the result as a dictionary with one key: "summarization."


    """

    # Call the OpenAI API with the provided prompt and configuration
    response = openai.chat.completions.create(
        model=model,
        seed=1,
        messages=[
            {"role": "system", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )

    # Extract the response text
    tasks = response.choices[0].message.content
    
    return tasks


transcript = open("transcript/test_transcript.txt", "r")
#Extract and print the tasks
def clean_json_string(json_string):
    # Remove Markdown code block syntax
    json_string = re.sub(r'```json\s*', '', json_string)
    json_string = re.sub(r'\s*```', '', json_string)
    
    # Remove any leading/trailing whitespace
    json_string = json_string.strip()
    
    return json_string

# Extract the tasks
tasks = extract_tasks(transcript)

# Clean the JSON string
cleaned_tasks = clean_json_string(tasks)

# Print the cleaned tasks string
# print("Cleaned tasks string:")
# print(cleaned_tasks)

# Try to parse the JSON string
try:
    tasks_dict = json.loads(cleaned_tasks)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    print("Content of cleaned tasks variable:")
    print(cleaned_tasks)
    # If parsing fails, we'll create a simple dictionary with the raw string
    tasks_dict = {"raw_output": cleaned_tasks}

# Create the 'task' directory if it doesn't exist
os.makedirs('summarization', exist_ok=True)

# Save the tasks as a JSON file
with open('summarization/summarization.json', 'w') as f:
    json.dump(tasks_dict, f, indent=4)

#print("Tasks have been saved to task/extracted_tasks.json")


