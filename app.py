import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

class Survey:
    def __init__(self):

        if 'run_num' not in st.session_state:
            st.session_state.run_num = 0

        # This hides the menu drop down
        hide_menu_style = """
                       <style>
                       #MainMenu {visibility: hidden;}
                       </style>
                       """
        st.markdown(hide_menu_style, unsafe_allow_html=True)
        # Initializing the Google sheets connection for the data and demographics survey
        self.spreadsheet_id1 = '1c0S-VhmH_tJbZ_DWkF1TCdFg9XhP4-f3xhTdfzzq6xk'
        self.sheet1 = self.initialize_connection()

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

        self.col1, self.col2, self.col3 = st.columns((1, 2, 1))


    @st.cache_resource
    def initialize_connection(_self):
        the_secrets = os.path.join(os.getcwd(), 'secret_account.json')
        creds1 = service_account.Credentials.from_service_account_file(
            the_secrets,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                    ],
                )
        service1 = build('sheets', 'v4', credentials=creds1)
        return service1.spreadsheets()

    def control(self):
        if st.session_state.run_num == 0:
           self.run_survey()
        elif st.session_state.run_num == 1:
            self.run_thanks()

    def run_survey(self):
        st.session_state.run_num += 1
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha:
            with st.form("info"):
                st.title("Prospective research participant information")
                st.write("Please enter your first name, last name, and an email we may contact you at.")
                st.text_input("What is your first name?", key='fname')
                st.text_input("What is your last name?", key='lname')
                st.text_input("What is your email?", key='email')
                st.form_submit_button("Submit", on_click=self.submit_survey)

    def submit_survey(self):
        # This is what updates Google sheets
        self.container_captcha.empty()
        stuff = [
            [st.session_state.fname, st.session_state.lname, st.session_state.email]]
        res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                          range="Sheet1!A:C", valueInputOption="USER_ENTERED",
                                          insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()

    def run_thanks(self):
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha:
            st.write("Thanks! you will be contacted shortly.")



if __name__ == "__main__":
    gm = Survey()
    gm.control()
