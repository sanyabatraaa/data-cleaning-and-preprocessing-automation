import streamlit as st
import requests
import pandas as pd
import json

FASTAPI_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI-Powered Data Cleaning", layout="wide")
st.sidebar.header("Data Source Selection")
data_source = st.sidebar.radio(
    "Select Data Source:",
    ["CSV/Excel", "Database Query", "API Data"],
    index=0
)

st.markdown("""
# **AI-Powered Data Cleaning**
*Clean your data effortlessly using AI-powered processing!*
""")

def display_cleaned_data(response):
    if response.status_code == 200:
        st.subheader("Raw API Response (Debugging)")
        response_data = response.json()
        st.json(response_data)
        try:
            cleaned_data_raw = response_data.get("cleaned_data", response_data)
            if isinstance(cleaned_data_raw, str):
                cleaned_data = pd.DataFrame(json.loads(cleaned_data_raw))
            else:
                cleaned_data = pd.DataFrame(cleaned_data_raw)
            st.subheader("Cleaned Data:")
            st.dataframe(cleaned_data)
        except Exception as e:
            st.error(f"Error converting response to DataFrame: {e}")
    else:
        st.error(f"Failed to clean data. Error: {response.text}")

# ============ CSV/Excel Upload ============ #
if data_source == "CSV/Excel":
    st.subheader("Upload File for Cleaning")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("### Raw Data Preview:")
        st.dataframe(df)

        if st.button("Clean Data"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{FASTAPI_URL}/clean-data", files=files)
            display_cleaned_data(response)

# ============ Database Query ============ #
elif data_source == "Database Query":
    st.subheader("Enter Database Query")
    db_url = st.text_input("Database connection URL", "postgresql://user:password@localhost:5432/db")
    query = st.text_area("Enter SQL Query", "SELECT * FROM my_table")

    if st.button("Fetch and Clean Data"):
        response = requests.post(
            f"{FASTAPI_URL}/clean-db",
            json={"db_url": db_url, "query": query}
        )
        display_cleaned_data(response)

# ============ External API ============ #
elif data_source == "API Data":
    st.subheader("Fetch Data from API")
    api_url = st.text_input("Enter API Endpoint:", "https://jsonplaceholder.typicode.com/posts")

    if st.button("Fetch and Clean Data"):
        response = requests.post(
            f"{FASTAPI_URL}/clean-api",
            json={"api_url": api_url}
        )
        display_cleaned_data(response)
