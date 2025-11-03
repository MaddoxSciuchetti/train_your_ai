from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st 
import sqlite3
import time
load_dotenv()
import threading
import subprocess
st.set_page_config(layout="wide")


#saving data
    #openai response to the image (wrong)
    #textfield next to it where i can write my response (corected)
    #image

class Handwerk:

    def __init__(self):
        self.conn = sqlite3.connect("/Users/maddoxsciuchetti/p-BSB/Handwerk_vision.py/frontend/Handwerk.db", isolation_level=None)
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.client = OpenAI()
        self.col1, self.col2, self.col3 = st.columns(3)
        

    def layout(self):
        with self.col1:
            st.title("Welcome")
            st.header("Train your own AI")
            self.uploaded_file = st.file_uploader("Upload file")

    def upload(self):

        with self.col2:
            try:

                if self.uploaded_file is not None:      
                    flag = True
                    file_name = self.uploaded_file.name
                    self.uploaded_file_path = os.path.join("/Users/maddoxsciuchetti/p-BSB/Handwerk_vision.py/sources", file_name)

                    with open(self.uploaded_file_path, "wb") as f:
                        f.write(self.uploaded_file.getbuffer())
                        st.success(f"Check")
                        
                    if flag == True:
                        st.image(self.uploaded_file_path, width=400)
                            
                    else: 
                        print("Upload file before proceeding")
            except Exception:
                print("wait")
            except ValueError:
                print("wait")


    def api(self):

        try:
            self.file = self.client.files.create(
                    file=open(self.uploaded_file_path, "rb"),
                    purpose="user_data"
                )
        except Exception:
            return ("still waiting")
        except ValueError:
            print("Wait")
        

    def api_response(self):

        try:

            response = self.client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_image",
                                "file_id": self.file.id,
                            },
                            {
                                "type": "input_text",
                                "text": "Identify the object in the image sent. write no more than three words",
                            },
                        ]
                    }
                ]
            )

            self.output = response.output_text
        except ValueError:
            print("wait")
        except Exception: 
            print("wait")

    def user_correction(self):
        with self.col1:

            try:
            
                st.text_area(label="Output Data:", value=self.output, height=350)   
                user_correction = st.text_input("What is it actually?")
                #submitting to database


                if st.button("Upload data"):
                    self.conn.execute(f'INSERT INTO data VALUES ("{self.output}", "{user_correction}", "{self.uploaded_file_path}")')

            except Exception:
                print("wait")


    def video(self):

        with self.col3:
            video_file = open("/Users/maddoxsciuchetti/p-BSB/Handwerk_vision.py/sources/MOV to MP4.mp4", "rb")
            video_bytes = video_file.read()
            return st.video(video_bytes, width=400)

    def data(self):

        infomation = self.conn.execute('SELECT * FROM data').fetchall()
        print(infomation)

mad = Handwerk()
mad.layout()
mad.video()
mad.upload()
mad.api()
mad.api_response()
mad.user_correction()
mad.data()




