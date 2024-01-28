import base64
import os
from pathlib import Path
from typing import List
from pydantic import BaseModel
import secrets

from llama_index.multi_modal_llms import GeminiMultiModal
from llama_index.program import MultiModalLLMCompletionProgram
from llama_index.output_parsers import PydanticOutputParser
from llama_index import SimpleDirectoryReader

import streamlit as st

from PIL import Image
import json

from decouple import config

import json


GOOGLE_API_KEY = config("GOOGLE_API_KEY")
MODEL_NAME = "models/gemini-pro-vision"


class ApplicantDetails(BaseModel):
    """Extract this information from the given image"""
    name: str
    professional_profile: str
    education: str
    skills: str
    email: str
    phone_number: str


prompt_template_str = """\
    Extract the following information from the CV provided to you. Do not paragraph the content of the CV.
    Only return to me what is written on the CV with no modifications, in case you do not konw what was written\
        just say I don't know and do not generate random filler text.
"""


def structed_response_gemini(
    output_class: ApplicantDetails,
    image_documents: list,
    prompt_template_str: str,
    model_name: str = MODEL_NAME,
):
    print("here")
    gemini_llm = GeminiMultiModal(
        api_key="AIzaSyDBQto8ebBKVnsPukmN6E7ELXaaAWCQ64Y",
        model_name=model_name
    )
    print("heer 2")
    llm_program = MultiModalLLMCompletionProgram.from_defaults(
        output_parser=PydanticOutputParser(output_cls=output_class),
        image_documents=image_documents,
        prompt_template_str=prompt_template_str,
        multi_modal_llm=gemini_llm,
        verbose=True
    )

    print("here 3")

    response = llm_program()
    return response


def get_details_from_multimodal_gemini(uploaded_image):
    # print(uploaded_image)
    # print(uploaded_image)
    for image_doc in uploaded_image:
        data_list = []
        structured_response = structed_response_gemini(
            output_class=ApplicantDetails,
            image_documents=[image_doc],
            prompt_template_str=prompt_template_str,
            model_name=MODEL_NAME
        )

        for r in structured_response:
            data_list.append(r)

        data_dict = dict(data_list)

        return data_dict


uploaded_file = st.file_uploader(
    "Choose a Image file", accept_multiple_files=False, type=["png", "jpg"])

if uploaded_file is not None:
    st.toast('File upload successful!', icon='🎉')
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)

    with st.spinner("Loading, please wait"):
        st.warning("Loading...")

        if (uploaded_file.type) == "image/jpeg":
            file_type = "jpg"
        else:
            file_type = "png"

        # save image
        os.makedirs("images", exist_ok=True)
        filename = f"{secrets.token_hex(8)}.{file_type}"
        with open(f"images/{filename}", "wb") as f:
            f.write(bytes_data)

        file_path = f"images/{filename}"

        # resize image
        img = Image.open(file_path)
        img = img.resize((500, 500))
        img.save(file_path)

        # load images
        images_documents = SimpleDirectoryReader(
            input_files=["/home/mani1911/Documents/Pragyan-Hack/CTY-NOW-2024/uploads/4c82e5ae1f279cac2b79.png"]).load_data()
        try:
            response = get_details_from_multimodal_gemini(
                uploaded_image=images_documents)
            
            # store processed information
            with open("/home/mani1911/Documents/Pragyan-Hack/CTY-NOW-2024/app/cv_submissions/data/data_store.jsonl", "a") as f:
                f.write(json.dumps({"doc": ', '.join(
                    [f"{key}: {value}" for key, value in response.items()])}) + "\n")

            # sidebar
            with st.sidebar:
                st.markdown(f'''
                            :green[Name]: {response.get("name", "Unknown")} \n
                            :green[Professional Profile]: :{response.get("professional_profile", "Unknwon")} \n
                            :green[Email Address]: {response.get("email", "Unknown")} \n
                            :green[Phone]: {response.get("phone_number", "Unknown")} \n
                            '''
                            )

                st.markdown('''
                            **Education**\n
                            ''')
                for education in response.get("education", []).split("\n"):
                    st.markdown(f'''
                                - {education}
                                ''')

                st.markdown('''
                            **Skills**\n
                            ''')
                for skill in response.get("skills", []).split("\n"):
                    st.markdown(f'''
                                - {skill}
                                ''')
        except Exception as e:
            print(e)
