import streamlit as st
from transformers import MarianTokenizer, MarianMTModel
import json 


# Load JSON data
with open('tasks/extracted_tasks.json', 'r') as f:
        data_extractor = json.load(f)
        
with open('summarization/summarization.json', 'r') as f:
        summary = json.load(f)

# Function to load the model and tokenizer with caching
@st.cache_resource
def load_model_and_tokenizer(model_name):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return model, tokenizer

# Load the model and tokenizer only once
mname = "marefa-nlp/marefa-mt-en-ar"
model, tokenizer = load_model_and_tokenizer(mname)

def translate_text(input_text):
    translated_tokens = model.generate(**tokenizer.prepare_seq2seq_batch([input_text], return_tensors="pt"))
    translated_text = [tokenizer.decode(t, skip_special_tokens=True) for t in translated_tokens]
    return translated_text[0]

# Function to recursively translate JSON content
def translate_json_content(content):
    if isinstance(content, dict):
        return {key: translate_json_content(value) for key, value in content.items()}
    elif isinstance(content, list):
        return [translate_json_content(item) for item in content]
    elif isinstance(content, str):
        return translate_text(content)
    else:
        return content
    

# Translate the extracted tasks
translated_json_data_extractor= translate_json_content(data_extractor)
translated_json_summary= translate_json_content(summary)


with open("translation/translated_json_data_extractor.json", "w", encoding="utf-8") as file1:
    json.dump(translated_json_data_extractor, file1, ensure_ascii=False, indent=4)

with open("translation/translated_json_summary.json", "w", encoding="utf-8") as file2:
    json.dump(translated_json_summary, file2, ensure_ascii=False, indent=4)

print("Translation and saving completed!")