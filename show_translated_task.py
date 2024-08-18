import streamlit as st
import json
def display_summary():
    # Load JSON data (assuming you will load from a file)
    with open('translation/translated_json_data_extractor.json', 'r',encoding="utf-8") as f:
        data_extractor = json.load(f)
    with open('translation/translated_json_summary.json', 'r',encoding="utf-8") as f:
        summary = json.load(f)

    st.title("Meeting Tasks Overview")
    st.header("Meeting Summary")
    st.write(summary["summarization"]["description"])
    st.subheader("Main Points")
    st.write("\n".join(f"- {point}" for point in summary["summarization"]["main_points"]))
    st.subheader("Decisions Made")
    st.write("\n".join(f"- {decision}" for decision in summary["summarization"]["decisions_made"]))
    st.subheader("Action Items")
    st.write("\n".join(f"- {action_item}" for action_item in summary["summarization"]["action_items"]))

    # Create two columns
    col1, col2 = st.columns(2)

    # Display simple tasks in the left column
    with col1:
        st.header("Simple Tasks")
        for task in data_extractor["simple_tasks"]:
            with st.expander(f"{task['task']}"):
                st.write(f"**Objective:** {task['instructions']['objective']}")
            st.write("---")

    # Display complex tasks in the right column
    with col2:
        st.header("Complex Tasks")
        for task in data_extractor["complex_tasks"]:
            with st.expander(f"{task['task']}"):
                st.write(task["description"])
            st.write("---")

display_summary()