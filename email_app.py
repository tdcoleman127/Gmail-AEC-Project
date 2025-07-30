import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="AEC Demo Dashboard", page_icon=":letterbox:", layout="wide")

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
st.title("📭 Email-esque Dashboard for AEC Demo")

# Sidebar for folders
st.sidebar.header("📁 Normal Folders")

# Get unique folders and email counts


sideCol, mainCol = st.columns([1, 3])

with sideCol:
    # Normal folders
    st.header("📂 Folders")
    base_folders = ["Inbox", "Notifications", "Work", "Personal", "Sent"]
    smart_folders = ["Work-Social", "Networking", "Work-Urgents"]
    
    # Count emails for all folders
    folders = {}
    for email in st.session_state.emails:
        folder = email['folder']
        if folder not in folders:
            folders[folder] = {'total': 0, 'unread': 0}
        folders[folder]['total'] += 1
        if not email['read']:
            folders[folder]['unread'] += 1

    # Always show base folders first
    for folder_name in base_folders:
        counts = folders.get(folder_name, {'total': 0, 'unread': 0})
        unread_badge = f" ({counts['unread']})" if counts['unread'] > 0 else ""
        if st.button(f"{folder_name}{unread_badge}", key=f"folder_{folder_name}"):
            st.session_state.selected_folder = folder_name
            st.session_state.selected_email = None
    
    # Initialize smart folders state if not exists
    if 'smart_folders_visible' not in st.session_state:
        st.session_state.smart_folders_visible = False
    if 'smart_folders_initialized' not in st.session_state:
        st.session_state.smart_folders_initialized = False
    if 'smart_emails' not in st.session_state:
        st.session_state.smart_emails = []

    st.divider()
    # Button to classify or shuffle
    if st.button("*G-Organize*"):
        if not st.session_state.smart_folders_initialized:
            # First press: Create copies of some emails for smart folders
            base_emails = [email for email in st.session_state.emails if email['folder'] in base_folders]
            selected_emails = random.sample(base_emails, min(15, len(base_emails)))  # Select up to 15 emails
            
            # Create copies for smart folders
            st.session_state.smart_emails = []
            for email in selected_emails:
                smart_email = email.copy()
                smart_email['id'] = f"smart_{email['id']}"  # New unique ID
                smart_email['folder'] = random.choice(smart_folders)
                st.session_state.smart_emails.append(smart_email)
            
            st.session_state.smart_folders_initialized = True
            st.session_state.smart_folders_visible = True
        else:
            # Subsequent presses: Shuffle between smart folders
            for email in st.session_state.smart_emails:
                email['folder'] = random.choice(smart_folders)
        
        st.rerun()

    # Display smart folders section if visible
    if st.session_state.smart_folders_visible:
        st.header("Smart Categories")
        # Count smart emails
        smart_counts = {}
        for email in st.session_state.smart_emails:
            folder = email['folder']
            if folder not in smart_counts:
                smart_counts[folder] = {'total': 0, 'unread': 0}
            smart_counts[folder]['total'] += 1
            if not email['read']:
                smart_counts[folder]['unread'] += 1

        for smart_folder in smart_folders:
            counts = smart_counts.get(smart_folder, {'total': 0, 'unread': 0})
            unread_badge = f" ({counts['unread']})" if counts['unread'] > 0 else ""
            if st.button(f"{smart_folder}{unread_badge}", key=f"smart_{smart_folder}"):
                st.session_state.selected_folder = smart_folder
                st.session_state.selected_email = None

    # Update emails list to include both original and smart emails
    if st.session_state.smart_folders_visible:
        st.session_state.emails = [e for e in st.session_state.emails if e['folder'] in base_folders] + st.session_state.smart_emails


with mainCol:
    st.header("📧 Emails")
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["📧 Email List", "📝 Compose", "⚙️ Settings"])

    with tab1:
        # Filter emails by selected folder
        filtered_emails = [email for email in st.session_state.emails if email['folder'] == st.session_state.selected_folder]
        
        # Email list header
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.subheader(f"{st.session_state.selected_folder} ({len(filtered_emails)} emails)")
        with col2:
            if st.button("🔄 Refresh"):
                st.rerun()
        with col3:
            if st.button("🗑️ Delete Selected"):
                st.warning("Delete functionality would go here")

        # Search and filters
        search_term = st.text_input("🔍 Search emails:", placeholder="Search by sender or subject...")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            show_unread_only = st.checkbox("Show unread only")
        with col2:
            show_starred_only = st.checkbox("Show starred only")
        with col3:
            sort_by = st.selectbox("Sort by:", ["Date", "Sender", "Subject"])

        # Apply filters
        display_emails = filtered_emails.copy()
        
        if search_term:
            display_emails = [email for email in display_emails 
                            if search_term.lower() in email['sender'].lower() or 
                                search_term.lower() in email['subject'].lower()]
        
        if show_unread_only:
            display_emails = [email for email in display_emails if not email['read']]
        
        if show_starred_only:
            display_emails = [email for email in display_emails if email['starred']]

        # Sort emails
        if sort_by == "Date":
            display_emails.sort(key=lambda x: x['timestamp'], reverse=True)
        elif sort_by == "Sender":
            display_emails.sort(key=lambda x: x['sender'])
        elif sort_by == "Subject":
            display_emails.sort(key=lambda x: x['subject'])

        # Email list display
        st.divider()
        
        for email in display_emails[:20]:  # Show first 20 emails
            # Email row
            col1, col2, col3, col4, col5 = st.columns([0.5, 0.5, 3, 2, 1])
            
            with col1:
                # Checkbox for selection
                selected = st.checkbox("", key=f"select_{email['id']}", label_visibility="collapsed")
            
            with col2:
                # Star button
                star_icon = "⭐" if email['starred'] else "☆"
                if st.button(star_icon, key=f"star_{email['id']}"):
                    email['starred'] = not email['starred']
                    st.rerun()
            
            with col3:
                # Sender and subject
                read_style = "" if email['read'] else "**"
                if st.button(f"{read_style}{email['sender']}{read_style}", 
                            key=f"email_{email['id']}", 
                            use_container_width=True):
                    st.session_state.selected_email = email['id']
                    email['read'] = True
            
            with col4:
                # Subject preview
                st.write(f"{email['subject'][:40]}...")
            
            with col5:
                # Timestamp
                st.write(email['timestamp'].strftime("%m/%d"))

        # Email detail view
        if st.session_state.selected_email is not None:
            selected_email = next((email for email in st.session_state.emails 
                                if email['id'] == st.session_state.selected_email), None)
            
            if selected_email:
                st.divider()
                st.subheader("📖 Email Details")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**From:** {selected_email['sender']}")
                    st.write(f"**Subject:** {selected_email['subject']}")
                    st.write(f"**Date:** {selected_email['timestamp'].strftime('%B %d, %Y at %I:%M %p')}")
                
                with col2:
                    # Move to folder dropdown
                    new_folder = st.selectbox("Move to folder:", 
                                            list(folders.keys()), 
                                            index=list(folders.keys()).index(selected_email['folder']))
                    if st.button("Move Email"):
                        selected_email['folder'] = new_folder
                        st.success(f"Email moved to {new_folder}")
                        st.rerun()
                
                st.write("**Email Content:**")
                st.write(selected_email['preview'])
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("Reply"):
                        st.info("Reply functionality would go here")
                with col2:
                    if st.button("Forward"):
                        st.info("Forward functionality would go here")
                with col3:
                    if st.button("Archive"):
                        st.info("Archive functionality would go here")
                with col4:
                    if st.button("Delete"):
                        st.info("Delete functionality would go here")

    with tab2:
        st.subheader("✍️ Compose New Email")
        
        # Compose form
        recipient = st.text_input("To:", placeholder="recipient@example.com")
        subject = st.text_input("Subject:", placeholder="Email subject")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            cc = st.text_input("CC:", placeholder="cc@example.com")
        with col2:
            priority = st.selectbox("Priority:", ["Normal", "High", "Low"])
        
        body = st.text_area("Message:", placeholder="Type your email here...", height=300)
        
        # Attachment placeholder
        st.write("📎 Attachments:")
        uploaded_file = st.file_uploader("Choose files", accept_multiple_files=True)
        
        # Send buttons
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("📤 Send"):
                if recipient and subject and body:
                    st.success("Email sent successfully!")
                else:
                    st.error("Please fill in all required fields")
        
        with col2:
            if st.button("💾 Save Draft"):
                st.info("Email saved as draft")

    with tab3:
        st.subheader("⚙️ Email Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Display Settings**")
            emails_per_page = st.slider("Emails per page:", 10, 50, 20)
            show_preview = st.checkbox("Show email preview", value=True)
            auto_refresh = st.checkbox("Auto-refresh emails")
            
            st.write("**Notification Settings**")
            desktop_notifications = st.checkbox("Desktop notifications")
            sound_notifications = st.checkbox("Sound notifications")
        
        with col2:
            st.write("**Account Settings**")
            signature = st.text_area("Email signature:", 
                                    placeholder="Best regards,\nYour Name")
            
            st.write("**Folder Settings**")
            auto_sort = st.checkbox("Auto-sort emails")
            if auto_sort:
                st.info("Emails will be automatically sorted into folders based on rules")
