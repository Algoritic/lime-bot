# Import necessary libraries and modules
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe, Agent
from pandasai.llm.openai import OpenAI
import openai

from decouple import config
import base64
from FetchResults import *

def get_data(survey_id):
    # # get session key
    username = config("LIMESURVEY_USERNAME") 
    password = config("LIMESURVEY_PASSWORD") 
    session = MPulseSessionManager(username, password, base_url=config("LIMESURVEY_BASE_URL"))
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
openai.api_key = config("OPENAI_API_KEY")

# Set page configuration and title for Streamlit
st.set_page_config(page_title="Lime Bot", page_icon="📄", layout="wide")

# Add header with title and description
st.markdown(
    '<p style="display:inline-block;font-size:40px;font-weight:bold;">💡 Lime Bot </p>'
    ' <p style="display:inline-block;font-size:16px;">This is an AI-powered '
    'chatbot that can be used to analyze and provide insights on your survey responses. Users can '
    'provide the survey ID, then view the data, and have interactive conversations with the AI model '
    'to obtain valuable information and answers related to the selected survey<br><br></p>',
    unsafe_allow_html=True
)

def chat_with_csv(df, prompt):
    llm = OpenAI(api_token=config("OPENAI_API_KEY"))
    agent = Agent([df], config={"llm": llm})
    result = agent.chat(prompt)
    return result

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
        data = pd.read_csv(input_csv, delimiter=";")
        st.dataframe(data, use_container_width=True)

    with col2:
        st.info("Chat Below")
        input_text = st.text_area("Enter your query")

        if input_text is not None:
            if st.button("Chat", help="Click to chat with the survey"):
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