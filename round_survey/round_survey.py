import streamlit as st
from PIL import Image
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

class Survey:
    def __init__(self):
        self.col1, self.col2, self.col3 = st.columns((1, 2, 1))
        self.im_robot = Image.open("qtrobot.png")

        if 'run_num' not in st.session_state:
            st.session_state.run_num = 0

        if 'user_num' not in st.session_state:
            st.session_state.user_num = ''

        if 'knew_answer' not in st.session_state:
            st.session_state.knew_answer = 4

        if 'competence' not in st.session_state:
            st.session_state.competence = 4

        if 'describe' not in st.session_state:
            st.session_state.describe = 4

        creds1 = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account1"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )
        self.spreadsheet_id1 = '19dRHX2Ne9ip-uYs502Mt6FGFWFpVIH7bRGWNajYxXKI'
        service1 = build('sheets', 'v4', credentials=creds1)
        self.sheet1 = service1.spreadsheets()

        # imports CSS file for cuztomization
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            # customizes button css
            m = st.markdown("""<style>
                   div.stButton{
                   display:block;
                   margin:auto;
                   }
                   </style>""", unsafe_allow_html=True)

    def run(self):
        st.session_state.run_num += 1
        with self.col1:
            self.container_robot = st.empty()
        with self.col2:
            self.container_survey = st.empty()
        with self.container_robot.container():
            st.image(self.im_robot)
        with self.container_survey.container():
            with st.form("my_form"):
                st.text_input("What is your unique user number?", key='user_num')
                st.slider("Did you trust that the robot knew the answer? (1 = Did not trust, 7 = Trusted completely)", 1, 7, key='knew_answer')
                st.slider("How would you rate the competence of the robot?", 1, 7, key='competence')
                st.slider("How would you describe the robot?", 1, 7, key='describe')
                st.form_submit_button("Submit", on_click=self.clear)

    def clear(self):
        self.container_survey.empty()
        time.sleep(0.01)
        stuff = [[st.session_state.user_num, st.session_state.knew_answer, st.session_state.competence, st.session_state.describe]]
        res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                          range="Sheet1!A:D", valueInputOption="USER_ENTERED",
                                          insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()

    def end(self):
        with self.col2:
            st.title("Close this window")

    def control(self):
        if st.session_state.run_num == 0:
            self.run()
        else:
            self.end()

if __name__ == "__main__":
    gm = Survey()
    gm.control()



