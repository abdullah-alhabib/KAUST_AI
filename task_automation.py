import json
import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


# Notion API credentials
NOTION_API_TOKEN = 'secret_ahUR1ReYO8rA60yxhIhXnUFf6050ISBs4pD1FIAm0fp'
NOTION_CAL_ID = 'aaa61a766037461897d5de5ec42749fe'
NOTION_TASKS_ID = '1479954f9d8a47508a5bdd7818b37f63'

NOTION_API_URL = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_notion_task(task_title, task_assigned_to=None, task_due_date=None):
    data = {
        "parent": {"database_id": NOTION_TASKS_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": task_title
                        }
                    }
                ]
            }
        }
    }
    
    # Only add "Assigned To" field if task_assigned_to is provided
    if task_assigned_to:
        data["properties"]["Assigned To"] = {
            "rich_text": [
                {
                    "text": {
                        "content": task_assigned_to
                    }
                }
            ]
        }
    
    # Only add "Due Date" field if task_due_date is provided
    if task_due_date:
        data["properties"]["Due Date"] = {
            "date": {
                "start": task_due_date
            }
        }

    # Make the request to create the task in Notion
    response = requests.post(NOTION_API_URL, headers=headers, json=data)
    
    # Handle the response
    if response.status_code == 200:
        print(f"Task '{task_title}' created successfully in Notion.")
    else:
        print(f"Failed to create task '{task_title}' in Notion: {response.text}")



def create_notion_event(event_title, event_date, event_time):
    # Convert time to 24-hour format
    event_time_24hr = datetime.strptime(event_time, "%I:%M %p").strftime("%H:%M:%S")

    # Combine date and time in ISO 8601 format
    iso_date_time = f"{event_date}T{event_time_24hr}"

    data = {
        "parent": {"database_id": NOTION_CAL_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": event_title
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                    "start": iso_date_time
                }
            }
        }
    }

    response = requests.post(NOTION_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Event '{event_title}' created successfully in Notion.")
    else:
        print(f"Failed to create event '{event_title}' in Notion: {response.text}")


def send_email(to_email, subject, body, from_email="alotaibifahad23@gmail.com", app_password='-----'):

    # Create the email message object
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Use TLS (Transport Layer Security)

        # Login to your Gmail account using the App Password
        server.login(from_email, app_password)

        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent successfully to {to_email}!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        # Close the connection to the server
        server.quit()

