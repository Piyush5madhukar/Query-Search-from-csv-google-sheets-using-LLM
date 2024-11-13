import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread
import requests
import time
import io
from dotenv import load_dotenv
import os

load_dotenv()

SERPAPI_KEY=os.getenv('SERPAI_API_KEY')
SERPAPI_URL = "https://serpapi.com/search"

GEMINI_API_KEY =os.getenv('GEMINI_API_KEY')

def extract_information_with_llm(column_content, user_query, search_results):
    """Send the column content and user query to Gemini API for an informed response."""
    try:
        combined_results = "\n".join([f"Title: {result['title']}\nSnippet: {result['snippet']}\nLink: {result['link']}\n" for result in search_results])
        full_prompt = f"Given the following content, answer the user's query.\n\nPrimary Question (Column Content): {column_content}\n\nUser Query: {user_query}\n\nSupporting Information:\n{combined_results}"

        data = {"contents": [{"parts": [{"text": full_prompt}]}]}
        headers = {"Content-Type": "application/json"}
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        
        response = requests.post(f"{endpoint}?key={GEMINI_API_KEY}", headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            extracted_info = response_json['candidates'][0]['content']['parts'][0]['text'].strip()
            return extracted_info
        else:
            st.error(f"Gemini API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while processing with Gemini: {e}")
        return None

def search_web(query):
    """Perform a web search using SerpAPI."""
    try:
        params = {"engine": "google", "q": query, "api_key": SERPAPI_KEY}
        response = requests.get(SERPAPI_URL, params=params)
        data = response.json()
        if "organic_results" in data:
            return [{"title": result["title"], "link": result["link"], "snippet": result["snippet"]} for result in data["organic_results"]]
        else:
            st.error("No search results found.")
            return []
    except Exception as e:
        st.error(f"Error during web search: {e}")
        return []

def load_google_sheets_data(google_sheet_url):
    """Load data from Google Sheets using gspread."""
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        credentials = Credentials.from_service_account_file("testing-441607-e97e541eb7bf.json", scopes=scope)
        client = gspread.authorize(credentials)
        sheet_id = google_sheet_url.split("/")[5]
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)
        return pd.DataFrame(worksheet.get_all_records())
    except Exception as e:
        st.error(f"An error occurred while loading Google Sheets data: {e}")
        return None

def main():
    st.title("Dashboard for File Upload and Google Sheets Connection")

    st.subheader("Upload a CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    st.subheader("Connect to Google Sheets")
    google_sheet_url = st.text_input("Enter Google Sheet URL")
    auth_button = st.button("Authenticate and Load Data")

    data_source = None

    if uploaded_file is not None:
        csv_data = pd.read_csv(uploaded_file)
        st.write("Data Preview from CSV:")
        st.dataframe(csv_data)

        if 'column_to_select' not in st.session_state:
            st.session_state.column_to_select = csv_data.columns[0]  
        column_to_select = st.selectbox("Select main column", csv_data.columns, index=csv_data.columns.get_loc(st.session_state.column_to_select), key="column_select")
        st.session_state.column_to_select = column_to_select
        data_source = csv_data

    elif auth_button and google_sheet_url:
        try:
            scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

            credentials = Credentials.from_service_account_file(
                "testing-441607-e97e541eb7bf.json",
                scopes=scope
            )
            client = gspread.authorize(credentials)

            sheet_id = google_sheet_url.split("/")[5]
            sheet = client.open_by_key(sheet_id)
            worksheet = sheet.get_worksheet(0)

            google_sheet_data = pd.DataFrame(worksheet.get_all_records())
            st.write("Data Preview from Google Sheets:")
            st.dataframe(google_sheet_data)

            if 'column_to_select' not in st.session_state:
                st.session_state.column_to_select = google_sheet_data.columns[0]  
            
            column_to_select = st.selectbox("Select main column", google_sheet_data.columns, index=google_sheet_data.columns.get_loc(st.session_state.column_to_select), key="column_select")
            st.session_state.column_to_select = column_to_select
            data_source = google_sheet_data
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if data_source is not None:
        st.subheader("Supportive Query for Column Content")
        user_prompt = st.text_input("Enter your query (e.g., 'What is the revenue of {item}?')")

        results = []

        if user_prompt and column_to_select:
            st.write("Results:")
            for item in data_source[column_to_select]:
                primary_question = item
                query = user_prompt.replace("{item}", str(item))
                st.write(f"Primary Question: '{primary_question}'")
                st.write(f"Generated Query: '{query}'")
                
                search_results = search_web(query)
                if search_results:
                    extracted_info = extract_information_with_llm(primary_question, user_prompt, search_results)
                    if extracted_info:
                        st.write(f"Extracted Information: {extracted_info}")
                        results.append({"Primary Question": primary_question, "User Query": query, "Extracted Information": extracted_info})
                else:
                    st.write("No results found.")
                    results.append({"Primary Question": primary_question, "User Query": query, "Extracted Information": "No results found"})
                
                time.sleep(1)  

        if results:
            results_df = pd.DataFrame(results)
            st.write("All Results:")
            st.dataframe(results_df)

            csv_buffer = io.StringIO()
            results_df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            csv_binary = csv_buffer.getvalue().encode('utf-8')

            st.download_button(
                label="Download Extracted Information as CSV",
                data=csv_binary,
                file_name="extracted_information.csv",
                mime="text/csv"
            )


if __name__ == "__main__":
    main()
