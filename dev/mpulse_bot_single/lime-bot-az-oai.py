# Import necessary libraries and modules
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe, Agent
from pandasai.llm.openai import OpenAI
from pandasai.llm.azure_openai import AzureOpenAI
import openai

from dotenv import load_dotenv
import base64
from FetchResults import *

OPENAI_API_KEY = "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"

# Get API key
# OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

def get_data(survey_id):
    # # get session key
    username = "pluginManager"
    password = "w4Gu6ctRvCHm"
    session = MPulseSessionManager(username, password, base_url="https://mpulse.maybanksandbox.com")
    session_key = session.get_session_key()

    # run api to get survey responses

    api = MPulseAPI()
    method = "export_responses"
    params = [session_key, survey_id, "csv", "en", "all", "full", "long"] # 148545

    response = api.make_request(method, params)
    response_data = response.json()
    results = Process.decode_base64_from_dict(response_data, type='csv', name=survey_id)
    return results

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY
AZURE_OPENAI_API_KEY = "c939e1dcd3fb47399ef1a18f849631b3"
# Set page configuration and title for Streamlit
st.set_page_config(page_title="M-Pulse Bot", page_icon="📄", layout="wide")

# Add header with title and description
st.markdown(
    '<p style="display:inline-block;font-size:40px;font-weight:bold;">💡 M-Pulse Bot </p>'
    ' <p style="display:inline-block;font-size:16px;">This is an AI-powered '
    'chatbot that can be used to analyze and provide insights on your survey responses. Users can '
    'provide the survey ID, then view the data, and have interactive conversations with the AI model '
    'to obtain valuable information and answers related to the selected survey<br><br></p>',
    unsafe_allow_html=True
)

def chat_with_csv(df, prompt):
    # llm = OpenAI(api_token=OPENAI_API_KEY)
    llm = AzureOpenAI(api_token=AZURE_OPENAI_API_KEY,
                      azure_endpoint="https://mbb-gen-ai.openai.azure.com/openai/deployments/gpt-35-t-16k/chat/completions?api-version=2023-07-01-preview",
                      api_base="https://mbb-gen-ai.openai.azure.com/", 
                      api_version="2023-06-01-preview", 
                      deployment_name="gpt-35-t-16k", is_chat_model=True)
    # pandas_ai = SmartDataframe(llm)

    # df = SmartDataframe(df, config={"llm": llm})
    agent = Agent([df], config={"llm": llm})
    # result = pandas_ai.run(df, prompt=prompt)
    result = agent.chat(prompt)
    # print(result)
    return result

# input_csv = st.file_uploader("Upload your CSV file", type=['csv'])
# survey_id = st.number_input("Enter Survey ID", min_value=1, format="%d")
survey_id = st.text_input("Enter Survey ID", 1234)

# Display the Survey ID
if survey_id:
    get_data(survey_id)
    st.write(f"You are Chatting with {survey_id}")
input_csv = f'{survey_id}.csv'
if input_csv is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("Survey Responses Loaded Successfully")
        # data = pd.read_csv(input_csv, na_values=["N/A", ""], header=None, delimiter=";")
        data = pd.read_csv(input_csv, delimiter=";")
        st.dataframe(data, use_container_width=True)

    with col2:
        st.info("Chat Below")
        input_text = st.text_area("Enter your query")

        if input_text is not None:
            if st.button("Chat", help="Click to chat with the survey", type="primary"):
                st.info("Your Query: " + input_text)
                result = chat_with_csv(data, input_text)
                # Check if the result contains an image path
                if ".png" in result:  # Assuming image paths end with ".png"
                    image_path = result  # Assign the path directly
                    st.image(image_path, caption="Chart generated from your query")  # Display the image
                else:
                    st.success(result)

# Hide Streamlit header, footer, and menu
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""

# Apply CSS code to hide header, footer, and menu
st.markdown(hide_st_style, unsafe_allow_html=True)