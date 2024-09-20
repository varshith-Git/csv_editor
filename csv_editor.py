import streamlit as st
import pandas as pd

# Title of the app
st.title("Dynamic CSV Editor")

# Password protection
password = st.text_input("Enter the password to access the file upload:", type="password")

# Password to access the app
required_password = "nttdata"

# Check if the correct password is entered
if password == required_password:
    st.success("Password accepted. You can now upload a CSV file.")

    # File upload section
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Display the original dataframe
        st.subheader("Original Data")
        st.write(df)

        # Make dynamic changes
        st.subheader("Modify Data")

        # Column renaming section
        st.write("### Edit Column Names")
        new_col_names = {}
        for col in df.columns:
            new_col_names[col] = st.text_input(f"Rename column '{col}':", value=col)

        # Apply new column names
        if st.button("Update Column Names"):
            df.rename(columns=new_col_names, inplace=True)
            st.success("Column names updated successfully.")
            st.write(df)

        # Value replacement section
        st.write("### Replace Values in Columns")
        col_options = st.selectbox("Select column to update values:", df.columns)
        value_to_change = st.text_input("Value to replace:")
        new_value = st.text_input("New value:")

        if st.button("Update Values"):
            df[col_options] = df[col_options].replace(value_to_change, new_value)
            st.success("Values updated successfully.")
            st.write(df)

        # Date format change section
        st.write("### Change Date Format")
        date_col = st.selectbox(
            "Select column to change date format:", df.select_dtypes(include=['datetime', 'object']).columns)

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

        selected_format = st.selectbox("Select date format:", list(date_formats.keys()))

        if st.button("Change Date Format"):
            try:
                # Convert selected column to datetime
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                # Apply selected date format
                df[date_col] = df[date_col].dt.strftime(date_formats[selected_format])
                st.success(f"Date format for '{date_col}' changed to {selected_format}.")
            except Exception as e:
                st.error(f"Error changing date format: {e}")

            st.write(df)

        # Download the modified dataframe as a CSV without index
        st.download_button(
            label="Download Modified CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="modified_data.csv",
            mime="text/csv"
        )
else:
    st.error("Please enter the correct password to access the file upload.")
