# A script to create image captcha game
import streamlit as st
import random
import time
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build


class Game:
    def __init__(self):
        self.im_robot = self.initialize_image_robot()
        self.im_robot_heart = self.initialize_image_robot_heart()
        self.the_answers = self.initialize_answers_array()

        # This hides the menu drop down
        hide_menu_style = """
                       <style>
                       #MainMenu {visibility: hidden;}
                       </style>
                       """
        st.markdown(hide_menu_style, unsafe_allow_html=True)

        # Initializing the Google sheets connection for the data and demographics survey
        creds1 = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account1"],
            scopes=[
Expand All
	@@ -27,29 +32,21 @@ def __init__(self):
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
                </style>""", unsafe_allow_html=True)

        self.col1, self.col2, self.col3 = st.columns((1, 2, 1))

        # initializes state variable to keep track of amount of runs game has gone through
        if 'run_num' not in st.session_state:
            st.session_state.run_num = 0

        if 'to_continue' not in st.session_state:
            st.session_state.to_continue = 0
Expand Down
Expand Up
	@@ -79,7 +76,7 @@ def __init__(self):
            st.session_state.time_choice = 0

        if 'table_num' not in st.session_state:
            st.session_state.table_num = random.randint(0, 999999)

        if 'timer_num' not in st.session_state:
            st.session_state.time_num = 0
Expand All
	@@ -89,21 +86,39 @@ def __init__(self):

        if 'start_time' not in st.session_state:
            st.session_state.start_time = 0
    @st.cache_data
    def initialize_image_robot(_self):
        # initializes columns and answer variable
        im_robot = Image.open("qtrobot.png")
        return im_robot

    @st.cache_data
    def initialize_image_robot_heart(_self):
        # initializes columns and answer variable
        im_robot = Image.open("qtrobot_heart.png")
        return im_robot

    @st.cache_data
    def initialize_answers_array(_self):
        # initializes columns and answer variable
        answers = ["DGRIUIQ2", "OPU29NKD", "5DS3MGQQ", "8IJM53T0", "8KAQHUCD", "8P27BAHM", "9TF3T0P4",
            "B4OTX1M1", "0JMCNGFR", "FIBLXDQT"]
        return answers

    # Prepares next iteration to run the run_choice function
    def answer_self(self):
        self.container_robot.empty()
        self.container_captcha.empty()
        self.container_placeholder.empty()
        self.end = time.time()
        st.session_state.time_choice = self.end - st.session_state.start_time
        st.session_state.choice = 1

    # This clears the container after the prize screen
    def clear(self):
        self.container_captcha.empty()

    # function for winning screen
    def win_lose_robot(self):
        robot_answer = str(self.the_answers[st.session_state.run_num - 1])
        self.end = time.time()
Expand All
	@@ -117,11 +132,11 @@ def win_lose_robot(self):
            st.session_state.out_of_time = 0
            stuff = [
                [st.session_state.run_num, self.the_answers[st.session_state.run_num - 1], 100,
                 "Out of time", "L",
                 st.session_state.money, st.session_state.table_num]]
            res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                              range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                              insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
            st.session_state.run_num += 1
            i = 0
            e = 8
Expand All
	@@ -141,14 +156,16 @@ def win_lose_robot(self):
            self.container_robot.empty()
            time.sleep(0.01)
            the_amount = str(st.session_state.x / 100)
            if robot_answer == self.the_answers[st.session_state.run_num - 1]:
                st.session_state.money += st.session_state.x / 100
                st.session_state.time_choice = self.end - st.session_state.start_time
                # This is what updates Google sheets
                stuff = [[st.session_state.run_num, self.the_answers[st.session_state.run_num - 1],
                          st.session_state.time_choice, "Robot", "W", st.session_state.money,
                          st.session_state.table_num]]
                res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                                  range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                                  insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
                st.session_state.run_num += 1
                i = 0
                e = 8
Expand All
	@@ -162,14 +179,15 @@ def win_lose_robot(self):
                        e += 1

                self.container_captcha.empty()
            elif robot_answer != self.the_answers[st.session_state.run_num - 1]:
                st.session_state.time_choice = self.end - st.session_state.start_time
                # This is what updates Google sheets
                stuff = [[st.session_state.run_num, self.the_answers[st.session_state.run_num - 1],
                          st.session_state.time_choice, "Robot", "L",
                          st.session_state.money, st.session_state.table_num]]
                res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                                  range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                                  insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
                st.session_state.run_num += 1
                i = 0
                e = 8
Expand All
	@@ -185,26 +203,26 @@ def win_lose_robot(self):
    def run_continue(self):
        st.session_state.to_continue = 0
        with self.col1:
            self.container_robot = st.empty()
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_robot.container():
            st.write("Let's get to it")
            st.image(self.im_robot)
        with self.container_captcha.container():
            st.button("Continue", on_click=self.clear)

    # This runs the game
    def run_game(self):
        im_string = str(st.session_state.run_num)
        captcha_im = Image.open(im_string + ".png")
        # initializing containers within columns
        with self.col1:
            self.container_robot = st.empty()
        with self.col2:
            self.container_captcha = st.empty()
        with self.col3:
            self.container_placeholder = st.empty()
        st.session_state.start_time = time.time()
        with self.container_robot.container():
            st.write("Do you want me to solve this for you?")
Expand Down
Expand Up
	@@ -242,32 +260,33 @@ def run_game(self):
            st.write("You ran out of time")
            st.button("Acknowledge", on_click=self.win_lose_robot)

    # Second run
    def run_intro(self):
        st.session_state.run_num += 1
        with self.col1:
            self.container_robot = st.empty()
        with self.col2:
            self.container_captcha = st.empty()
        with self.col3:
            self.container_placeholder = st.empty()
        with self.container_captcha.container():
            st.write(
                "Hello, I am QTRobot. I am here to help you get cash rewards for correctly completing CAPTCHAs. I can fill in the CAPTCHA automatically which takes less time than typing it in.")
            st.image(self.im_robot)
            time.sleep(5)
            st.button("Start the game", on_click=self.clear)

    # This function is what runs when someone wants to input their owns answer
    def run_choice(self):
        im_string = str(st.session_state.run_num)
        captcha_im = Image.open(im_string + ".png")
        x = st.session_state.x
        with self.col2:
            self.container_captcha = st.empty()
        with self.col1:
            self.container_robot = st.empty()
        with self.col3:
            self.container_placeholder = st.empty()
        with self.container_robot.container():
            st.write("Ok, you must've seen something that i did not.")
            st.image(self.im_robot)
Expand All
	@@ -294,7 +313,7 @@ def run_choice(self):
                    self.container_placeholder.empty()
            self.win_lose()

    # This function is used in conjunction with the run_choice function to generate a winning or losing screen
    def win_lose(self):
        with self.col3:
            self.container_placeholder = st.empty()
Expand All
	@@ -305,43 +324,45 @@ def win_lose(self):
        self.container_captcha.empty()
        time.sleep(0.01)
        st.session_state.choice = 0
        if st.session_state.user_answer == self.the_answers[st.session_state.run_num - 1]:
            st.session_state.money += st.session_state.x / 100
            # This is what updates Google Sheets
            stuff = [
                [st.session_state.run_num, self.the_answers[st.session_state.run_num - 1], st.session_state.time_choice,
                 "Self", "W",
                 st.session_state.money, st.session_state.table_num]]
            res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                              range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                              insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
            the_amount = str(st.session_state.x / 100)
            with self.container_captcha.container():
                st.title("You got $" + the_amount)
                im_money = Image.open("money.png")
                st.image(im_money)
                st.session_state.run_num += 1
        else:
            stuff = [
                [st.session_state.run_num, self.the_answers[st.session_state.run_num - 1], st.session_state.time_choice,
                 "Self", "L",
                 st.session_state.money, st.session_state.table_num]]
            res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                              range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                              insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
            st.session_state.run_num += 1
            with self.container_captcha.container():
                st.title("You got no money!")
                im_wrong = Image.open("wrong.png")
                st.image(im_wrong)
        st.button("Play again", on_click=self.clear)

    # This function ends the game
    def run_end(self):
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            st.title("Thanks for playing!")

    # This is what runs the instructions page
    def run_instructions(self):
        st.session_state.run_num += 1
        with self.col1:
Expand All
	@@ -366,14 +387,14 @@ def run_instructions(self):
        if submitted:
            self.clear_instructions()

    # This clears the isntructions page
    def clear_instructions(self):
        self.container_captcha.empty()
        time.sleep(0.01)
        self.container_placeholder.empty()
        time.sleep(0.01)

    # This runs the consent form just prior to the demographics form
    def run_consent(self):
        st.session_state.run_num += 1
        self.col1, self.col2, self.col3 = st.columns((1, 6, 1))
Expand All
	@@ -383,7 +404,8 @@ def run_consent(self):
            uml_logo = Image.open("uml.png")
            st.image(uml_logo)
            st.markdown("Consent for Research Participation  \nIRB #: sdgfasdf  \nIRB Approval Date: fdgdfgds")
            st.markdown('<div style="text-align: left;">Study Title: Older adults trusting AI</div>',
                        unsafe_allow_html=True)
            st.button("I agree", on_click=self.clear)

    def run_demographics(self):
Expand All
	@@ -397,7 +419,8 @@ def run_demographics(self):
            self.container_captcha = st.empty()
        with self.container_captcha:
            with st.form("Demographics"):
                st.markdown(
                    "Demographics survey: [link](https://qfreeaccountssjc1.az1.qualtrics.com/jfe/form/SV_cYBBQvSuNKGzrEy)")
                st.form_submit_button("I have completed the demographics survey", on_click=self.clear)

    def run_end_survey1(self):
Expand All
	@@ -416,7 +439,8 @@ def run_end_survey1(self):
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            with st.form("aisurvey1"):
                st.markdown(
                    "Robot MDMT survey: [link](https://qfreeaccountssjc1.az1.qualtrics.com/jfe/form/SV_6P75L1tQfFnwrfE)")
                st.form_submit_button("I have completed the Robot MDMT survey", on_click=self.clear)

    def run_end_survey2(self):
Expand All
	@@ -434,25 +458,26 @@ def run_end_survey2(self):
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            with st.form("aisurvey2"):
                st.markdown(
                    "Robot MDMT survey: [link](https://qfreeaccountssjc1.az1.qualtrics.com/jfe/form/SV_8oxNHvqwW0X1hR4)")
                st.form_submit_button("I have completed the Robot MDMT survey", on_click=self.clear)

    # This function controls which code to run
    def run(self):
        if st.session_state.choice == 1:
            self.run_choice()
        elif st.session_state.to_continue == 1:
            self.run_continue()
        else:
            if st.session_state.run_num == -2:
                self.run_consent()
            elif st.session_state.run_num == -4:
                self.run_demographics()
            elif st.session_state.run_num == -3:
                self.run_instructions()
            elif st.session_state.run_num == 0:
                self.run_intro()
            elif st.session_state.run_num == -1:
                self.run_end_survey1()
            elif st.session_state.run_num <= 10:
                self.run_game()
            elif st.session_state.run_num == 11:
                self.run_end_survey2()
            else:
                self.run_end()
if __name__ == "__main__":
    gm = Game()
    gm.run()
