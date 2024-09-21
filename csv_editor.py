import streamlit as st
import pandas as pd
from datetime import datetime

# Title of the app
st.title("CSV Column Name Cleaner and Date Formatter")

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Correct password to access the app
required_password = "nttdata"

# Initialize session state to manage successful login
if "login_successful" not in st.session_state:
    st.session_state.login_successful = False

# Display the password input section only if not logged in
if not st.session_state.login_successful:
    # Password input field
    password = st.text_input("Enter the password to access the file upload:", type="password")

    # Check if the correct password is entered
    if password == required_password:
        st.session_state.login_successful = True
        st.success("Login successful! You can now upload CSV files.")
    elif password:
        st.error("Incorrect password. Please try again.")

# Show the file upload section only if the login is successful
if st.session_state.login_successful:
    # File upload section with support for multiple files
    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)

    # Define date format rules for specific files and columns
    date_format_rules = {
        'asmt_metric_result.csv': {
            'sys_created_on': '%Y-%m-%d %H:%M:%S',
            'sys_updated_on': '%Y-%m-%d %H:%M:%S',
            'instance_sys_created_on': '%Y-%m-%d %H:%M:%S',
        },
        'awa_interaction_work_item.csv': {
            'doc_assigned_at': '%Y-%m-%d %H:%M:%S',
            'doc_closed_at': '%Y-%m-%d %H:%M:%S',
            'doc_sys_created_on': '%Y-%m-%d %H:%M:%S',
            'wi_sys_created_on': '%Y-%m-%d %H:%M:%S',
            'doc_live_handoff_time': '%Y-%m-%d %H:%M:%S',
            'wi_offered_on': '%Y-%m-%d %H:%M:%S',
            'doc_opened_at': '%Y-%m-%d %H:%M:%S',
            'doc_state_changed_on': '%Y-%m-%d %H:%M:%S',
            'doc_sys_updated_on': '%Y-%m-%d %H:%M:%S',
            'wi_sys_updated_on': '%Y-%m-%d %H:%M:%S',
            'wi_state_changed_on': '%Y-%m-%d %H:%M:%S',
        },
        'interaction.csv': {
            'closed_at': '%Y-%m-%d %H:%M:%S',
            'assigned_at': '%Y-%m-%d %H:%M:%S',
            'sys_created_on': '%Y-%m-%d %H:%M:%S',
            'live_handoff_time': '%Y-%m-%d %H:%M:%S',
            'opened_at': '%Y-%m-%d %H:%M:%S',
            'state_changed_on': '%Y-%m-%d %H:%M:%S',
            'sys_updated_on': '%Y-%m-%d %H:%M:%S',
        },
        'interaction_related_record.csv': {
            'task.opened_at': '%Y-%m-%d %H:%M:%S',
            'sys_created_on': '%Y-%m-%d %H:%M:%S',
            'sys_updated_on': '%Y-%m-%d %H:%M:%S',
            'interaction_opened_at': '%Y-%m-%d %H:%M:%S',
        },
        'incident.csv': {
            'u_sla_50_timestamp': '%Y-%m-%d %H:%M:%S',
            'proposed_on': '%Y-%m-%d %H:%M:%S',
            'promoted_on': '%Y-%m-%d %H:%M:%S',
            'u_ntt_sla_calculation': '%Y-%m-%d %H:%M:%S',
            'u_mi_accepted_rejected_time': '%Y-%m-%d %H:%M:%S',
            'reopened_time': '%Y-%m-%d %H:%M:%S',
            'u_impact_start_end_entered': '%Y-%m-%d %H:%M:%S',
            'u_impact_end': '%Y-%m-%d %H:%M:%S',
            'opened_at': '%Y-%m-%d %H:%M:%S',
            'sys_created_on': '%Y-%m-%d %H:%M:%S',
            'sys_updated_on': '%Y-%m-%d %H:%M:%S',
            'resolved_at': '%Y-%m-%d %H:%M:%S',
            'closed_at': '%Y-%m-%d %H:%M:%S',
        },
        'u_group_reassignment_logs.csv': {
            'u_task_closed_at': '%Y-%m-%d %H:%M:%S',
            'u_task_sys_updated_on': '%Y-%m-%d %H:%M:%S',
        },
        'm2m_kbtask.csv': {
            'task_closed_at': '%Y-%m-%d %H:%M:%S',
            'task_sys_created_on': '%Y-%m-%d %H:%M:%S',
            'task_sys_updated_on': '%Y-%m-%d %H:%M:%S',
            'task_opened_at': '%Y-%m-%d %H:%M:%S',
            'sys_created_on': '%Y-%m-%d %H:%M:%S',
        },
        'kb_Knowledge.csv': {
            'sys_created_on': '%Y-%m-%d %H:%M:%S',
            'sys_updated_on': '%Y-%m-%d %H:%M:%S',
        },
        'sla_breakdown_by_assignment.csv': {
            'end': '%Y-%m-%d %H:%M:%S',
        },
        'incident_sla.csv': {
            'taskslatable_end_time': '%Y-%m-%d %H:%M:%S',
        }
    }

    if uploaded_files:
        # Get today's date in the desired format (YYYYMMDD)
        today_date = datetime.now().strftime("%Y%m%d")

        for uploaded_file in uploaded_files:
            st.write(f"### File: {uploaded_file.name}")

            # Read the file content to check if it's empty
            try:
                content = uploaded_file.read()
                if not content:
                    st.error(f"The file '{uploaded_file.name}' is empty. Please upload a non-empty CSV file.")
                    continue
            except Exception as e:
                st.error(f"Error reading the file '{uploaded_file.name}': {e}")
                continue

            # Attempt to read the uploaded CSV file with various encodings
            df = None
            encodings = ['utf-8', 'latin1', 'ISO-8859-1']
            for encoding in encodings:
                try:
                    # Reset the file pointer to the beginning
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    break  # If successful, break out of the loop
                except (UnicodeDecodeError, pd.errors.EmptyDataError):
                    continue  # Try the next encoding

            # Check if the dataframe was successfully read
            if df is None:
                st.error(f"Failed to read the file: {uploaded_file.name}. The file might be empty or improperly formatted.")
                continue

            # Automatically replace periods in column names with underscores
            df.columns = [col.replace('.', '_') for col in df.columns]

            # Apply date format rules if applicable
            file_name = uploaded_file.name
            if file_name in date_format_rules:
                rules = date_format_rules[file_name]
                for col, desired_format in rules.items():
                    if col in df.columns:
                        # Allow user to apply the specified date format
                        st.write(f"Applying date format '{desired_format}' to column '{col}'")
                        df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime(desired_format)

            # Display the corrected dataframe
            st.subheader("Data with Corrected Column Names and Formats")
            st.write(df)

            # Extract the base name of the file without extension
            base_name = uploaded_file.name.rsplit('.', 1)[0]

            # Create the new file name with today's date appended
            modified_file_name = f"{base_name}_{today_date}.csv"

            # Download the modified dataframe as a CSV without index
            st.download_button(
                label=f"Download Modified CSV for {uploaded_file.name}",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=modified_file_name,
                mime="text/csv"
            )
