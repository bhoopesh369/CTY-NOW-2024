import os
import json
import shutil
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv
from enum import Enum
import time


api_host = os.environ.get("HOST", "127.0.0.1")
api_port = int(os.environ.get("PORT", 8000))


# Streamlit UI elements
st.title("🏷️ Real Time Multi-modal LLM App")

question = st.text_input(
    "Search for CV applicants",
    placeholder="Search for CV applicants"
)


# Handle Discounts API request if data source is selected and a question is provided
if question:
    url = f'http://{api_host}:{api_port}/'
    data = {"query": question}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.write("### Answer")
        st.write(response.json())
    else:
        st.error(
            f"Failed to send data to Discounts API. Status code: {response.status_code}")
