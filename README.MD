1)Project Description
This project is a Streamlit dashboard designed to allow users to upload a CSV file or connect to a Google Sheet. It enables querying data from these sources and augments the queries with web search results using SerpAPI. The dashboard integrates the Gemini API to process these search results and extract meaningful information, which is then presented to the user. The extracted data can be downloaded as a CSV file.



2)Setup Instructions

---Install Dependencies:

## Clone the repository or download the code.

##Navigate to the project folder and install the required dependencies using pip:
bash
Copy code---->pip install -r requirements.txt

#API Keys and Credentials:

You will need API keys for both the SerpAPI and Gemini API. Make sure to replace the keys in the code with your actual keys (see "API Keys and Environment Variables").


#Google Sheets Authentication:

Ensure you have a Google Service Account with access to your Google Sheets and download the credentials JSON file.
Update the path to the credentials file in the code (e.g., "testing-447817-e97e541eb7bf.json").

3)Usage Guide
Running the Application:

1)Start the Streamlit application by running the following command:
bash
Copy code ---->streamlit run app.py

2)Connecting Google Sheets:

Once the dashboard is loaded, you can enter the URL of a Google Sheet into the provided text input field.
Click on the "Authenticate and Load Data" button to connect to the Google Sheet and load the data into the dashboard.

OR

3)Uploading a CSV File:

You can also upload a CSV file through the dashboard interface. Once the file is uploaded, the data will be displayed in the dashboard.

4)Setting Up Search Queries:

After loading the data, enter a query in the "Supportive Query for Column Content" field (e.g., What is the revenue of {item}?).
The query will be dynamically populated for each item in the selected column.

5)Web Search and Extraction:

The system performs a web search for each generated query using SerpAPI and extracts relevant information via the LLM Gemini API.
The extracted information is displayed on the dashboard.

6)Download Results:

After the information has been extracted for all items, the results will be displayed in a table format.
You can download the results as a CSV file by clicking the "Download Extracted Information as CSV" button.


4)API Keys and Environment Variables

--SerpAPI:

Go to SerpAPI and create an account to get your API key.
Replace the placeholder key ("fdfb92f5--5a4aa0ac9b9ede4a4934f02-----48b809f8b") in the code with your actual key.

--Gemini API:

Sign up for access to the Gemini API via Google Cloud.
Replace the placeholder API key ("AIzaSjbacabcxachAcwVRscsK8PqtDia5A") with your actual API key in the code.

--Google Sheets Authentication:

Create a Service Account in Google Cloud and enable the Google Sheets API.
Download the JSON file with credentials and ensure the path is correct in the code.




----------------------------------------------------------------------------------

To set up Google Sheets API credentials and obtain the credentials.json file, follow these steps:

Step 1: Enable Google Sheets API
      : Go to Google Cloud Console: Visit Google Cloud Console.
      : Create a New Project:
      : In the Console, click on Select a project at the top.
      : Click New Project and name it as desired.
      : Click Create.
      : Enable Google Sheets API:
      : In the Google Cloud Console, go to APIs & Services > Library.
      : Search for "Google Sheets API".
      : Select Google Sheets API and click Enable.

Step 2: Set Up Service Account Credentials ->Create Service Account:

Go to APIs & Services > Credentials in the Console.
Click Create Credentials > Service Account.
Enter a name for your service account, and click Create and Continue.
Assign a Role (Optional for Sheets Access):

Under Select a role, choose a basic role like Viewer (or skip, if no role is required).
Click Continue and then Done.
Generate Service Account Key:

After creating the service account, go to the Credentials page in the Console.
Find your service account in the list, click on it, and navigate to the Keys tab.
Click Add Key > Create new key.
Choose JSON format and click Create.
A credentials.json file will download to your computer. Save this file securely.

Step 3: Share Google Sheets with the Service Account
Open the Google Sheet you want to access.
Click Share in the top right.
Copy the Service Account Email (available in the Google Cloud Console under the Service Account details).
Paste the Service Account Email in the Share with people and groups field in the Google Sheets sharing settings.
Click Send (if prompted to notify, you can skip).

Step 4: Add credentials.json to Your Project Directory
Move the credentials.json file to the directory where your Python script is located (or use the correct path as needed).
Make sure the file is accessible by your application.