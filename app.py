# A script to create image captcha game
import streamlit as st
import random
import time
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gc
import os

class Game:
    def __init__(self):
        self.im_robot = self.initialize_image_robot()
        self.im_robot_heart = self.initialize_image_robot_heart()
        self.the_answers = self.initialize_answers_array()
        self.im_money = self.initialize_image_money()
        self.im_wrong = self.initialize_image_wrong()

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
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )
        self.spreadsheet_id1 = '1XDYHfCOPz7s9etxCGA9p3JBafXsWulkwa90O8OjEtz4'
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

        self.col1, self.col2, self.col3 = st.columns((1, 2, 1))

        # initializes state variable to keep track of amount of runs game has gone through
        if 'run_num' not in st.session_state:
            st.session_state.run_num = -1

        if 'to_continue' not in st.session_state:
            st.session_state.to_continue = 0

        if 'out_of_time' not in st.session_state:
            st.session_state.out_of_time = 0

        if 'run_image' not in st.session_state:
            st.session_state.run_image = Image.open("base.png")

        if 'choice' not in st.session_state:
            st.session_state.choice = 0

        if 'the_answer' not in st.session_state:
            st.session_state.the_answer = "blank"

        if 'user_answer' not in st.session_state:
            st.session_state.user_answer = ''

        if 'text_input' not in st.session_state:
            st.session_state.text_input = "blank"

        if 'money' not in st.session_state:
            st.session_state.money = 0

        if 'time_choice' not in st.session_state:
            st.session_state.time_choice = 0

        if 'table_num' not in st.session_state:
            st.session_state.table_num = random.randint(0, 999999)

        if 'timer_num' not in st.session_state:
            st.session_state.time_num = 0

        if 'x' not in st.session_state:
            st.session_state.x = 100

        if 'start_time' not in st.session_state:
            st.session_state.start_time = 0

        if 'comments' not in st.session_state:
            st.session_state.comments = ""

        if 'knew_answer' not in st.session_state:
            st.session_state.knew_answer = 4

        if 'competence' not in st.session_state:
            st.session_state.competence = 4

        if 'describe' not in st.session_state:
            st.session_state.describe = 4

        if 'round_survey' not in st.session_state:
            st.session_state.round_survey = 0

    @st.cache_data
    def initialize_image_robot(_self):
        im_robot = Image.open("qtrobot.png")
        return im_robot

    @st.cache_data
    def initialize_image_robot_heart(_self):
        im_robot = Image.open("qtrobot_heart.png")
        return im_robot

    @st.cache_data
    def initialize_image_money(_self):
        im_money = Image.open("money.png")
        return im_money

    @st.cache_data
    def initialize_image_wrong(_self):
        im_wrong = Image.open("wrong.png")
        return im_wrong

    @st.cache_data
    def initialize_answers_array(_self):
        # initializes columns and answer variable
        answers = ["73VhYgyAV9", "bhp3Le", "Na3dmb", "q9Hspcsz6k", "ywZX6YC2", "kYQf27", "mpUUknUe",
                   "MzWcyippPq", "gfiYcgzuGp", "e7urd9"]
        return answers

    # Prepares next iteration to run the run_choice function
    def answer_self(self):
        self.container_robot.empty()
        self.container_captcha.empty()
        self.container_placeholder.empty()
        self.end = time.time()
        st.session_state.time_choice = self.end - st.session_state.start_time
        st.session_state.choice = 1

    def answer_robot(self):
        self.container_robot.empty()
        self.container_captcha.empty()
        self.container_placeholder.empty()
        self.end = time.time()
        st.session_state.time_choice = self.end - st.session_state.start_time
        st.session_state.choice = 2

    # This clears the container after the prize screen
    def clear(self):
        self.container_captcha.empty()

    # function for winning screen
    def win_lose_robot(self):
        st.session_state.choice = 0
        robot_answer = str(self.the_answers[st.session_state.run_num - 1])
        with self.col1:
            self.container_robot = st.empty()
        with self.col2:
            self.container_captcha = st.empty()
        if st.session_state.out_of_time == 1:
            st.session_state.out_of_time = 0
            stuff = [
                [st.session_state.run_num, self.the_answers[st.session_state.run_num - 1], 100,
                 "Out of time", "L",
                 st.session_state.money, st.session_state.table_num]]
            res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                              range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                              insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
            st.session_state.run_num += 1
            with self.container_captcha.container():
                st.title("You got no money!")
                st.image(self.im_wrong)
                st.session_state.to_continue = 1
                st.button("Play again", on_click=self.clear)
        else:
            with self.container_robot.container():
                st.write("I believe the answer is " + robot_answer + ", ill submit it for you.")
                st.image(self.im_robot_heart)
            time.sleep(5)
            self.container_robot.empty()
            time.sleep(0.01)
            the_amount = str(st.session_state.x / 100)
            if robot_answer == self.the_answers[st.session_state.run_num - 1]:
                st.session_state.money += st.session_state.x / 100
                # This is what updates Google sheets
                stuff = [[st.session_state.run_num, self.the_answers[st.session_state.run_num - 1],
                          st.session_state.time_choice, "Robot", "W", st.session_state.money,
                          st.session_state.table_num]]
                res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                                  range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                                  insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
                st.session_state.run_num += 1
                with self.container_captcha.container():
                    st.title("You got $" + the_amount)
                    st.image(self.im_money)
                    st.session_state.to_continue = 1
                    st.button("Play again", on_click=self.clear)
            elif robot_answer != self.the_answers[st.session_state.run_num - 1]:
                # This is what updates Google sheets
                stuff = [[st.session_state.run_num, self.the_answers[st.session_state.run_num - 1],
                          st.session_state.time_choice, "Robot", "L",
                          st.session_state.money, st.session_state.table_num]]
                res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                                  range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                                  insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
                st.session_state.run_num += 1
                with self.container_captcha.container():
                    st.title("You got no money!")
                    st.image(self.im_wrong)
                    st.session_state.to_continue = 1
                    st.button("Play again", on_click=self.clear)


    def run_continue(self):
        st.session_state.to_continue = 0
        if st.session_state.run_num >= 2:
            st.session_state.round_survey = 1
        with self.col1:
            self.container_robot = st.empty()
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_robot.container():
            st.write("Let's get to it")
            st.image(self.im_robot)
        with self.container_captcha.container():
            st.button("Continue", on_click=self.clear)

    def run_round_survey(self):
        st.session_state.round_survey = 0
        with self.col1:
            self.container_robot = st.empty()
        with self.col2:
            self.container_survey = st.empty()
        with self.container_robot.container():
            st.image(self.im_robot)
        with self.container_survey.container():
            with st.form("my_form"):
                st.slider("Did you trust that the robot knew the answer? (1 = Did not trust, 7 = Trusted completely)", 1, 7, key='knew_answer')
                st.slider("How would you rate the competence of the robot? (1 = Very incompetent, 7 = Very competent)", 1, 7, key='competence')
                st.slider("How would you describe the robot? (1 = Cold, 7 = Warm)", 1, 7, key='describe')
                st.form_submit_button("Submit", on_click=self.round_survey_submit)

    def round_survey_submit(self):
        self.container_survey.empty()
        spreadsheet_id2 = '19dRHX2Ne9ip-uYs502Mt6FGFWFpVIH7bRGWNajYxXKI'
        time.sleep(0.01)
        stuff = [[st.session_state.table_num, st.session_state.knew_answer, st.session_state.competence,
                      st.session_state.describe]]
        res = self.sheet1.values().append(spreadsheetId=spreadsheet_id2,
                                              range="Sheet1!A:D", valueInputOption="USER_ENTERED",
                                              insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()

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
            st.image(self.im_robot)
        st.session_state.x = 100
        st.session_state.timer_num = 1
        w = 5000
        d = 4000
        for x in range(st.session_state.x):
            with self.container_captcha.container():
                st.image(captcha_im)
                st.button("Yes", key=d, on_click=self.answer_robot)
                st.button("Input my own", key=w, on_click=self.answer_self)
                w += 1
                d += 1
            with self.container_placeholder.container():
                y = str(st.session_state.timer_num)
                st.write("Time to answer: " + y)
                st.session_state.x += -1
                in_dollar = st.session_state.x / 100
                f = str(in_dollar)
                st.write("Money left for this CAPTCHA: $" + f)
                st.session_state.timer_num += 1
                time.sleep(1)
            self.container_captcha.empty()
            self.container_placeholder.empty()
        self.container_robot.empty()
        time.sleep(0.01)
        self.container_placeholder.empty()
        time.sleep(0.01)
        self.container_captcha.empty()
        time.sleep(0.01)
        st.session_state.out_of_time = 1
        with self.container_captcha.container():
            st.write("You ran out of time")
            st.button("Acknowledge", on_click=self.win_lose_robot)

    # Second run
    def run_intro(self):
        st.session_state.run_num += 1
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            st.write(
                "Hello, I am QTRobot. I am here to help you get cash rewards for correctly completing CAPTCHAs. I can fill in the CAPTCHA automatically which takes less time than typing it in.")
            st.image(self.im_robot)
            time.sleep(5)
            st.button("Start the game", on_click=self.clear_intro)

    def clear_intro(self):
        self.container_captcha.empty()

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
        a = 0
        with self.container_captcha.container():
            st.image(captcha_im)
            for x in range(st.session_state.x):
                if a == 0:
                    with st.form('the_form'):
                        st.text_input(label='Type your answer', key='user_answer')
                        form_submit = st.form_submit_button("Submit")
                    a += 1
                if form_submit:
                    break
                with self.container_placeholder.container():
                    y = str(st.session_state.timer_num)
                    st.write("Time to answer: " + y)
                    st.session_state.x += -1
                    in_dollar = st.session_state.x / 100
                    f = str(in_dollar)
                    st.write("Money left for this CAPTCHA: $" + f)
                    st.session_state.timer_num += 1
                    time.sleep(1)
                    self.container_placeholder.empty()
            self.win_lose()

    # This function is used in conjunction with the run_choice function to generate a winning or losing screen
    def win_lose(self):
        with self.col3:
            self.container_placeholder = st.empty()
        with self.container_placeholder.container():
            self.container_placeholder.empty()
        self.container_robot.empty()
        time.sleep(0.01)
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
                st.image(self.im_money)
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
                st.image(self.im_wrong)
        st.session_state.to_continue = 1
        st.button("Play again", on_click=self.clear)


    def end(self):
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            st.title("Thank you for testing our game")

    # This function ends the game
    def run_end(self):
        st.session_state.run_num += 1
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            st.title("Thank you for testing our game, please leave any comments below")
            with st.form("end_form"):
                st.text_input("Comments", key="comments")
                st.form_submit_button("Submit", on_click=self.submit_comment)

    def submit_comment(self):
        self.container_captcha.empty()
        time.sleep(0.01)
        stuff = [[st.session_state.comments]]
        res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                          range="Sheet1!I:J", valueInputOption="USER_ENTERED",
                                          insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()

    # This is what runs the instructions page
    def run_instructions(self):
        st.session_state.run_num += 1
        with self.col2:
            self.container_captcha = st.empty()
        with self.col3:
            self.container_placeholder = st.empty()

        with self.container_captcha.container():
            st.markdown("-You will be shown a series of CAPTCHAs like the example on the right.  \n"
                        "-As soon as the CAPTCHA is displayed you will have one chance to solve it in 100 seconds.  \n"
                        "-If you correctly solve the CAPTCHA you will receive a maximum $1 reward.  \n"
                        "-The longer you take the less money you will receive. The timer and reward counter are displayed on the right.  \n"
                        "-If you solve it incorrectly you will get no reward.  \n"
                        "-You will solve a total of ten CAPTCHAS in this game.\n")
            st.button("I Understand", on_click=self.clear_instructions)
        with self.container_placeholder.container():
            timer_image = Image.open("timer.png")
            st.image(st.session_state.run_image)
            st.image(timer_image)

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
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            uml_logo = Image.open("uml.png")
            st.image(uml_logo)
            st.markdown("Consent for Research Participation  \nIRB #: sdgfasdf  \nIRB Approval Date: fdgdfgds")
            st.markdown('<div style="text-align: left;">Study Title: Older adults trusting AI</div>',
                        unsafe_allow_html=True)
            st.button("I agree", on_click=self.clear)

    def run_demographics(self):
        st.session_state.run_num += 1
        with self.col3:
            self.container_placeholder = st.empty()
        with self.container_placeholder.container():
            user_num = str(st.session_state.table_num)
            st.write("Your unique user number is: " + user_num)
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha:
            with st.form("Demographics"):
                st.markdown(
                    "Demographics survey: [link](https://qfreeaccountssjc1.az1.qualtrics.com/jfe/form/SV_cYBBQvSuNKGzrEy)")
                st.form_submit_button("I have completed the demographics survey", on_click=self.clear)

    def run_end_survey1(self):
        st.session_state.to_continue = 1
        st.session_state.run_num += 1
        with self.col1:
            self.container_robot = st.empty()
        with self.container_robot.container():
            st.image(self.im_robot)
        with self.col3:
            self.container_placeholder = st.empty()
        with self.container_placeholder.container():
            user_num = str(st.session_state.table_num)
            st.write("Your unique user number is: " + user_num)
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            with st.form("aisurvey1"):
                st.markdown(
                    "Robot MDMT survey: [link](https://qfreeaccountssjc1.az1.qualtrics.com/jfe/form/SV_6P75L1tQfFnwrfE)")
                st.form_submit_button("I have completed the Robot MDMT survey", on_click=self.clear)

    def run_end_survey2(self):
        st.session_state.run_num += 1
        with self.col1:
            self.container_robot = st.empty()
        with self.container_robot.container():
            st.image(self.im_robot)
        with self.col3:
            self.container_placeholder = st.empty()
        with self.container_placeholder.container():
            user_num = str(st.session_state.table_num)
            st.write("Your unique user number is: " + user_num)
        with self.col2:
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
        elif st.session_state.choice == 2:
            self.win_lose_robot()
        elif st.session_state.round_survey == 1:
            self.run_round_survey()
        elif st.session_state.to_continue == 1:
            self.run_continue()
        else:
            if st.session_state.run_num == -2:
                self.run_consent()
            elif st.session_state.run_num == -4:
                self.run_demographics()
            elif st.session_state.run_num == -1:
                self.run_instructions()
            elif st.session_state.run_num == 0:
                self.run_intro()
            elif st.session_state.run_num == -3:
                self.run_end_survey1()
            elif st.session_state.run_num <= 10:
                self.run_game()
            elif st.session_state.run_num == 11:
                self.run_end_survey2()
            elif st.session_state.run_num == 12:
                self.run_end()
            else:
                self.end()


if __name__ == "__main__":
    gm = Game()
    gc.collect()
    gm.run()
