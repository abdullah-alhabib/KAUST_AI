import streamlit as st
import json
from task_automation import send_email, create_notion_event, create_notion_task

# Function to get button text based on task type
def get_button_text(task_type):
    if task_type == "email":
        return "Send the email"
    elif task_type == "meeting":
        return "Schedule the meeting"
    elif task_type == "reminder":
        return "Set the reminder"
    else:
        return "Assign the task"  # Default for complex tasks

# Function to handle the task automation
def automate_task(task_key, task):
    # Only automate if this task hasn't been automated yet
    if not st.session_state.get(f"task_done_{task_key}"):
        task_type = task.get('type', 'complex')
        if task_type == 'email':
            send_email(
                to_email=task['instructions']['email_address'][0],
                subject=task['instructions']['subject'],
                body=task['instructions']['body']
            )
        elif task_type == 'meeting':
            create_notion_event(
                task['task'],
                task['instructions']['date'],
                task['instructions']['time']
            )
        elif task_type == 'reminder':
            create_notion_task(
                task_title=task['task'],
                task_assigned_to=task['instructions']['involved'],
                task_due_date=task['instructions']['date']
            )
        else:
            create_notion_task(
                task_title=task['task'],
                task_assigned_to=None,
                task_due_date=None
            )
        # Mark this task as done
        st.session_state[f"task_done_{task_key}"] = True
        st.success(f"Task '{task['task']}' has been automated.")
    else:
        st.warning(f"Task '{task['task']}' has already been automated.")

# Function to display more information based on the task type
def display_task_details(task):
    st.write(f"**Objective:** {task['instructions']['objective']}")
    
    # Display additional details based on task type
    if task['type'] == 'email':
        st.write(f"**Involved:** {task['instructions']['involve']}")
        st.write(f"**Email Addresses:** {task['instructions']['email_address']}")
        st.write(f"**Subject:** {task['instructions']['subject']}")
        st.write(f"**Body:** {task['instructions']['body']}")
        st.write(f"**Follow-Up:** {task['instructions']['follow-up']}")
    elif task['type'] == 'meeting':
        st.write(f"**Involved:** {task['instructions']['involve']}")
        st.write(f"**Date:** {task['instructions']['date']}")
        st.write(f"**Time:** {task['instructions']['time']}")
        st.write(f"**Location:** {task['instructions']['location']}")
    elif task['type'] == 'reminder':
        st.write(f"**Involved:** {task['instructions']['involve']}")
        st.write(f"**Date:** {task['instructions']['date']}")
        st.write(f"**Message:** {task['instructions']['message']}")
    else:
        st.write("No additional information available for this task.")

# Function to display the task summary and handle task automation
def display_summary():
    # Load JSON data
    with open('tasks/extracted_tasks.json', 'r') as f:
        data_extractor = json.load(f)
    with open('summarization/summarization.json', 'r') as f:
        summary = json.load(f)

    st.title("Meeting Overview")
    st.header("Meeting Summary")
    st.write(summary["summarization"]["description"])
    st.subheader("Main Points")
    st.write("\n".join(f"- {point}" for point in summary["summarization"]["main_points"]))
    st.subheader("Decisions Made")
    st.write("\n".join(f"- {decision}" for decision in summary["summarization"]["decisions_made"]))
    st.subheader("Action Items")
    st.write("\n".join(f"- {action_item}" for action_item in summary["summarization"]["action_items"]))

    # Create tabs with the specified arrangement
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 **Tasks Assigned**",
        "📅 **Meetings Planned**",
        "⏰ **Reminders Set**",
        "📧 **Emails Discussed**"
    ])

    # Display tasks that were assigned, including complex tasks
    with tab1:
        st.header("📝 **Tasks Assigned**")
        # Display simple tasks that don't fall into other categories
        for i, task in enumerate(data_extractor["simple_tasks"]):
            if task['type'] not in ['email', 'meeting', 'reminder']:
                task_key = f"task_{i}"
                with st.expander(f"{task['task']}"):
                    display_task_details(task)  # Display more task details
                    button_text = "Assign the task"
                    if st.button(button_text, key=task_key):
                        automate_task(task_key, task)  # Automate the task when button is clicked
                st.write("---")
        
        # Display complex tasks that were assigned
        for i, task in enumerate(data_extractor["complex_tasks"]):
            task_key = f"complex_{i}"
            with st.expander(f"{task['task']}"):
                st.write(task["description"])  # Display the description for complex tasks
                button_text = "Assign the task"  # All complex tasks are treated as generic tasks
                if st.button(button_text, key=task_key):
                    automate_task(task_key, task)  # Automate the task when button is clicked
            st.write("---")

    # Display meeting-related discussions
    with tab2:
        st.header("📅 **Meetings Planned**")
        for i, task in enumerate(data_extractor["simple_tasks"]):
            if task['type'] == 'meeting':
                task_key = f"meeting_{i}"
                with st.expander(f"{task['task']}"):
                    display_task_details(task)  # Display more task details
                    button_text = get_button_text(task['type'])
                    if st.button(button_text, key=task_key):
                        automate_task(task_key, task)  # Automate the task when button is clicked
                st.write("---")

    # Display reminder-related discussions
    with tab3:
        st.header("⏰ **Reminders Set**")
        for i, task in enumerate(data_extractor["simple_tasks"]):
            if task['type'] == 'reminder':
                task_key = f"reminder_{i}"
                with st.expander(f"{task['task']}"):
                    display_task_details(task)  # Display more task details
                    button_text = get_button_text(task['type'])
                    if st.button(button_text, key=task_key):
                        automate_task(task_key, task)  # Automate the task when button is clicked
                st.write("---")

    # Display email-related discussions
    with tab4:
        st.header("📧 **Emails Discussed**")
        for i, task in enumerate(data_extractor["simple_tasks"]):
            if task['type'] == 'email':
                task_key = f"email_{i}"
                with st.expander(f"{task['task']}"):
                    display_task_details(task)  # Display more task details
                    button_text = get_button_text(task['type'])
                    if st.button(button_text, key=task_key):
                        automate_task(task_key, task)  # Automate the task when button is clicked
                st.write("---")


