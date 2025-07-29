import streamlit as st

# Configure page
st.set_page_config(page_title="Email Dashboard", layout="wide")

# Sample data
emails = [
    {"sender": "john@company.com", "subject": "Meeting tomorrow", "folder": "Inbox"},
    {"sender": "sarah@team.com", "subject": "Project update", "folder": "Work"},
    {"sender": "alerts@github.com", "subject": "Security alert", "folder": "Notifications"},
]

folders = ["Inbox", "Work", "Personal", "Notifications"]

# Layout
col1, col2 = st.columns([1, 3])

# Sidebar - Folders
with col1:
    st.header("Folders")
    selected_folder = st.radio("", folders)

# Main area - Email list with tabs
with col2:
    st.header("Email Dashboard")
    
    tab1, tab2 = st.tabs(["Emails", "Compose"])
    
    with tab1:
        st.subheader(f"{selected_folder}")
        
        # Filter emails by folder
        folder_emails = [email for email in emails if email["folder"] == selected_folder]
        
        # Display emails
        for email in folder_emails:
            with st.container():
                st.write(f"**{email['sender']}** - {email['subject']}")
                st.divider()
    
    with tab2:
        st.subheader("Compose Email")
        recipient = st.text_input("To:")
        subject = st.text_input("Subject:")
        body = st.text_area("Message:")
        st.button("Send")