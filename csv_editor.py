import streamlit as st
import pandas as pd
from datetime import datetime

# Title of the app
st.title("CSV Column Name Cleaner")

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

            # Display the corrected dataframe
            st.subheader("Data with Corrected Column Names")
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
