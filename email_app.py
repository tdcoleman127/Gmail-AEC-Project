import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="AEC Demo Dashboard", page_icon=":tada:", layout="wide")

# Dummy data for emails
# Need Barbaros to provide the actual data
# Sample email data generator
def generate_sample_emails():
    senders = [
        "john.doe@company.com", "sarah.wilson@startup.io", "notifications@github.com",
        "team@slack.com", "billing@aws.com", "no-reply@linkedin.com",
        "updates@medium.com", "security@google.com", "newsletter@techcrunch.com"
    ]
    
    subjects = [
        "Q4 Budget Review Meeting", "Welcome to our platform!", "Security alert for your account",
        "Your weekly digest", "Invoice #12345", "New connection request",
        "Project update: Dashboard redesign", "Password reset requested", "Meeting reminder"
    ]
    
    emails = []
    for i in range(50):
        email = {
            "id": i,
            "sender": random.choice(senders),
            "subject": random.choice(subjects),
            "preview": f"This is a preview of email {i+1}. Lorem ipsum dolor sit amet...",
            "timestamp": datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23)),
            "read": random.choice([True, False]),
            "starred": random.choice([True, False]),
            "folder": random.choice(["Inbox", "Work", "Personal", "Notifications", "Sent"])
        }
        emails.append(email)
    
    return emails

# Initialize session state
if 'emails' not in st.session_state:
    st.session_state.emails = generate_sample_emails()

if 'selected_folder' not in st.session_state:
    st.session_state.selected_folder = "Inbox"

if 'selected_email' not in st.session_state:
    st.session_state.selected_email = None

# Main dashboard
st.title("📧 Email Dashboard")

# Sidebar for folders
st.sidebar.header("📁 Folders")

st.title("Let's party")

st.title("Email dashboard")