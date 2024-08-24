import openai
import json  
import os  
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
openai.api_key =st.secrets["OPENAI_KEY"]
model = config['model']
temperature = config['temperature']
max_tokens = config['max_tokens']
# print(f"model: {model}, temperature: {temperature}, max_tokens: {max_tokens}")

def extract_tasks(transcript):
    # Optimized Prompt for extracting and detailing tasks
    prompt = f"""
    You are an AI specialized in analyzing meeting transcripts. Below is a transcript of a meeting. Your task is to extract both complex and simple tasks mentioned in the meeting.

    Complex tasks are those that require multiple steps, coordination among team members, or significant time/resources. Simple tasks, on the other hand, are those that can be completed quickly with minimal effort, such as sending an email or setting up a meeting.

    For complex tasks:
    - List them with a brief description of what makes them complex.
    - task and their description.

    For simple tasks:
    - include the type of each task (e.g., email, meeting, reminder).
    - for type email the attibutues should be type , task,  instructions where has objective, involve , email address, subject, body, follow-up only do not add more.
    -for type meeting the attibutues should type, task and instructions where has objective, involve, date , time , duration , location and follow-up
    -for type reminder the attibutues should type, task and instructions where has objective, involve, date , time , message ,follow-up only 
    - List each task with detailed, actionable instructions that could be used by an automated system (like a Large Actions Model, LAM) to perform the task with minimal or no human interaction.
    - Include specific details such as the task objective, who is involved, any necessary information (like email addresses, dates, and times), and any follow-up actions that may be required.

    Here is the transcript:
    \"{transcript}\"

    Please return the tasks as a dictionary with two keys: "complex_tasks" and "simple_tasks". Each should contain a list of tasks with descriptions or detailed instructions.
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
os.makedirs('tasks', exist_ok=True)

# Save the tasks as a JSON file
with open('tasks/extracted_tasks.json', 'w') as f:
    json.dump(tasks_dict, f, indent=4)

#print("Tasks have been saved to task/extracted_tasks.json")
