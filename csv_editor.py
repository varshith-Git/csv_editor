import streamlit as st
import pandas as pd

# Title of the app
st.title("Dynamic CSV Editor")

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
        for uploaded_file in uploaded_files:
            st.write(f"### File: {uploaded_file.name}")

            # Attempt to read the uploaded CSV file with various encodings
            df = None
            encodings = ['utf-8', 'latin1', 'ISO-8859-1']
            for encoding in encodings:
                try:
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    break  # If successful, break out of the loop
                except UnicodeDecodeError:
                    continue  # Try the next encoding

            # Check if the dataframe was successfully read
            if df is None:
                st.error(f"Failed to read the file: {uploaded_file.name} due to encoding issues.")
                continue

            # Automatically replace periods in column names with underscores
            df.columns = [col.replace('.', '_') for col in df.columns]

            # Display the original dataframe with corrected column names
            st.subheader("Data with Corrected Column Names")
            st.write(df)

            # Make dynamic changes
            st.subheader("Modify Data")

            # Column renaming section
            st.write("### Edit Column Names")
            new_col_names = {}
            for col in df.columns:
                new_col_names[col] = st.text_input(f"Rename column '{col}' in {uploaded_file.name}:", value=col)

            # Apply new column names
            if st.button(f"Update Column Names in {uploaded_file.name}"):
                df.rename(columns=new_col_names, inplace=True)
                st.success("Column names updated successfully.")
                st.write(df)

            # Value replacement section
            st.write("### Replace Values in Columns")
            col_options = st.selectbox(f"Select column to update values in {uploaded_file.name}:", df.columns)
            value_to_change = st.text_input(f"Value to replace in {col_options} of {uploaded_file.name}:")
            new_value = st.text_input(f"New value for {col_options} of {uploaded_file.name}:")

            if st.button(f"Update Values in {uploaded_file.name}"):
                df[col_options] = df[col_options].replace(value_to_change, new_value)
                st.success("Values updated successfully.")
                st.write(df)

            # Date format change section
            st.write("### Change Date Format")
            date_col = st.selectbox(
                f"Select column to change date format in {uploaded_file.name}:", df.select_dtypes(include=['datetime', 'object']).columns)

            # Predefined date format options
            date_formats = {
                "Year-Month-Day (2024-09-20)": "%Y-%m-%d",
                "Day/Month/Year (20/09/2024)": "%d/%m/%Y",
                "Month-Day-Year (09-20-2024)": "%m-%d-%Y",
                "Day Month Year (20 Sep 2024)": "%d %b %Y",
                "Full Date (September 20, 2024)": "%B %d, %Y",
                "Day-Month-Year Hour:Minute (20-09-2024 14:30)": "%d-%m-%Y %H:%M",
                "Year-Month-Day Hour:Minute:Second (2024-09-20 14:30:00)": "%Y-%m-%d %H:%M:%S"
            }

            selected_format = st.selectbox(f"Select date format for {date_col} in {uploaded_file.name}:", list(date_formats.keys()))

            if st.button(f"Change Date Format in {uploaded_file.name}"):
                try:
                    # Convert selected column to datetime
                    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                    # Apply selected date format
                    df[date_col] = df[date_col].dt.strftime(date_formats[selected_format])
                    st.success(f"Date format for '{date_col}' in {uploaded_file.name} changed to {selected_format}.")
                except Exception as e:
                    st.error(f"Error changing date format: {e}")

                st.write(df)

            # Download the modified dataframe as a CSV without index
            st.download_button(
                label=f"Download Modified CSV for {uploaded_file.name}",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"modified_{uploaded_file.name}",
                mime="text/csv"
            )
