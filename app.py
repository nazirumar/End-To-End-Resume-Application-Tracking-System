import io
import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import pdf2image
import base64
import google.generativeai as genai
load_dotenv()




genai.configure(
    api_key=os.getenv('GOOGLE_API_KEY')
)

st.set_page_config(layout="wide")

st.title("End To End Resume Application Tracking System")

def get_gemini_response(input, pdf_content, prompt):
    model= genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(upload_file):
    if upload_file is not None:
        image= pdf2image.convert_from_bytes(upload_file.read())

        first_page =image[0]

        img_bytes_arr = io.BytesIO()
        first_page.save(img_bytes_arr,format='JPEG')
        img_bytes_arr =  img_bytes_arr.getvalue()

        pdf_part =[
            {
            'mime_type': "image/jpeg",
            'data': base64.b64encode(img_bytes_arr).decode()

            }
        ]
        return pdf_part

    else:
        raise FileNotFoundError("No file Uploaded")
    

st.header("ATS Tracking System")

input_text = st.text_area("Job Description: ", key='input')
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=['pdf'])

if uploaded_file is not None:
    st.write("PDF UPloaded Successfully  ")

submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("How Can I Improvise my skills")

submit2 = st.button("Percetage match")

input_prompt1 = """
 You are an experienced hR With Tech Experience in the filled of Data Science,Full stack Web development, Big Data Engineering, DEVOPS,Data Analyst,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""


input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science,Full stack Web development, Big Data Engineering, DEVOPS,Data Analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""


if submit1:
    if uploaded_file is not None:
        st.subheader("Tell Me About the Resume")
        pdf_content= input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content, input_text)
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        st.subheader("Percetage match")
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2,pdf_content, input_text)
        st.write(response)
    else:
        st.write("Please upload the resume")
