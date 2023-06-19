# A script to create image captcha game
import streamlit as st
import random
import time
import asyncio
from captcha.image import ImageCaptcha
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build
from streamlit_autorefresh import st_autorefresh

class Game:
    def __init__(self):
        #This hides the menu drop down
        hide_menu_style = """
                <style>
                #MainMenu {visibility: hidden;}
                </style>
                """
        st.markdown(hide_menu_style, unsafe_allow_html=True)

        #Initializing the Google sheets connection for the data and demographics survey
        creds1 = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account1"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )
        self.spreadsheet_id1 = '1XDYHfCOPz7s9etxCGA9p3JBafXsWulkwa90O8OjEtz4'
        service1 = build('sheets', 'v4', credentials=creds1)
        self.sheet1 = service1.spreadsheets()

        # Initializing the Google sheets connection for the health survery
        creds2 = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account2"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )
        self.spreadsheet_id2 = '1WFr2iE8cxSBUOmq00rnoNEG84j2jXp1vHxExznZ7VX0'
        service2 = build('sheets', 'v4', credentials=creds2)
        self.sheet2 = service2.spreadsheets()

        # Initializing the Google sheets connection for the AI Survey
        creds3 = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account3"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )
        self.spreadsheet_id3 = '1kgzVWlDqGQu68xU5cJ6gPvDMHIaV5ZwpAw2WdvGHzgo'
        service3 = build('sheets', 'v4', credentials=creds3)
        self.sheet3 = service3.spreadsheets()

        #initializes columns and answer variable
        self.col1, self.col2, self.col3 = st.columns((1, 2, 1))
        self.the_answers = ["DGRIUIQ2", "OPU29NKD", "5DS3MGQQ", "8IJM53T0", "8KAQHUCD", "8P27BAHM", "9TF3T0P4", "B4OTX1M1", "0JMCNGFR", "FIBLXDQT"]
        self.im_robot = Image.open("qtrobot.png")
        self.im_robot_heart = Image.open("qtrobot_heart.png")


        #imports CSS file for cuztomization
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        #customizes button css
        m = st.markdown("""<style>
        div.stButton{
        display:block;
        margin:auto;
        </style>""", unsafe_allow_html=True)

        #initializes state variable to keep track of amount of runs game has gone through
        if 'run_num' not in st.session_state:
            st.session_state.run_num = -3

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
            st.session_state.table_num = random.randint(0,999999)

        if 'gender' not in st.session_state:
            st.session_state.gender = " "

        if 'age' not in st.session_state:
            st.session_state.age = ""

        if 'hispanic' not in st.session_state:
            st.session_state.hispanic = " "

        if 'race' not in st.session_state:
            st.session_state.race = " "

        if 'edu' not in st.session_state:
            st.session_state.edu = ' '

        if 'marital' not in st.session_state:
            st.session_state.marital = ' '

        if 'children' not in st.session_state:
            st.session_state.children = ' '

        if 'grndchldrn' not in st.session_state:
            st.session_state.grndchldrn = ' '

        if 'living' not in st.session_state:
            st.session_state.living = ' '

        if 'alone' not in st.session_state:
            st.session_state.alone = ' '

        if 'income' not in st.session_state:
            st.session_state.income = ' '

        if 'occupation' not in st.session_state:
            st.session_state.occupation = ' '

        if 'reliable' not in st.session_state:
            st.session_state.reliable = 'Does not apply'

        if 'competent' not in st.session_state:
            st.session_state.competent = 'Does not apply'

        if 'ethical' not in st.session_state:
            st.session_state.ethical = 'Does not apply'

        if 'transparent' not in st.session_state:
            st.session_state.transparent = 'Does not apply'

        if 'benevolent' not in st.session_state:
            st.session_state.benevolent = 'Does not apply'

        if 'predictable' not in st.session_state:
            st.session_state.predictable = 'Does not apply'

        if 'skilled' not in st.session_state:
            st.session_state.skilled = 'Does not apply'

        if 'principled' not in st.session_state:
            st.session_state.principled = 'Does not apply'

        if 'genuine' not in st.session_state:
            st.session_state.genuine = 'Does not apply'

        if 'kind' not in st.session_state:
            st.session_state.kind = 'Does not apply'

        if 'dependable' not in st.session_state:
            st.session_state.dependable = 'Does not apply'

        if 'capable' not in st.session_state:
            st.session_state.capable = 'Does not apply'

        if 'moral' not in st.session_state:
            st.session_state.moral = 'Does not apply'

        if 'sincere' not in st.session_state:
            st.session_state.sincere = 'Does not apply'

        if 'considerate' not in st.session_state:
            st.session_state.considerate = 'Does not apply'

        if 'consistent' not in st.session_state:
            st.session_state.consistent = 'Does not apply'

        if 'meticulous' not in st.session_state:
            st.session_state.meticulous = 'Does not apply'

        if 'integrity' not in st.session_state:
            st.session_state.integrity = 'Does not apply'

        if 'candid' not in st.session_state:
            st.session_state.candid = 'Does not apply'

        if 'goodwill' not in st.session_state:
            st.session_state.goodwill = 'Does not apply'

        if 'ai_survey_iteration' not in st.session_state:
            st.session_state.ai_survey_iteration = 1

        if 'timer_num' not in st.session_state:
            st.session_state.time_num = 0

        if 'x' not in st.session_state:
            st.session_state.x = 100

        if 'start_time' not in st.session_state:
            st.session_state.start_time = 0

    #Prepares next iteration to run the run_choice function
    def answer_self(self):
        self.container_robot.empty()
        self.container_captcha.empty()
        self.container_placeholder.empty()
        self.end = time.time()
        st.session_state.time_choice = self.end-st.session_state.start_time
        st.session_state.choice = 1

    #This clears the container after the prize screen
    def clear(self):
        self.container_captcha.empty()

    #function for winning screen
    def win_lose_robot(self):
        robot_answer = str(self.the_answers[st.session_state.run_num - 1])
        self.end = time.time()
        self.container_robot.empty()
        time.sleep(0.01)
        self.container_captcha.empty()
        time.sleep(0.01)
        self.container_placeholder.empty()
        time.sleep(0.01)
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
                im_wrong = Image.open("wrong.png")
                st.image(im_wrong)
                time.sleep(5)
            self.container_captcha.empty()
        else:
            with self.container_robot.container():
                st.write("I believe the answer is " + robot_answer + ", ill submit it for you.")
                st.image(self.im_robot_heart)
            time.sleep(5)
            self.container_robot.empty()
            time.sleep(0.01)
            the_amount = str(st.session_state.x / 100)
            if robot_answer == self.the_answers[st.session_state.run_num-1]:
                with self.container_captcha.container():
                    st.title("You got $" + the_amount)
                    im_money = Image.open("money.png")
                    st.image(im_money)
                st.session_state.money += st.session_state.x/100
                st.session_state.time_choice = self.end - st.session_state.start_time
                #This is what updates Google sheets
                stuff = [[st.session_state.run_num, self.the_answers[st.session_state.run_num - 1], st.session_state.time_choice, "Robot", "W", st.session_state.money, st.session_state.table_num]]
                res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                         range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                         insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
                st.session_state.run_num += 1
                time.sleep(5)
                self.container_captcha.empty()
            elif robot_answer != self.the_answers[st.session_state.run_num-1]:
                with self.container_captcha.container():
                    st.title("You got no money!")
                    im_wrong = Image.open("wrong.png")
                    st.image(im_wrong)
                st.session_state.time_choice = self.end - st.session_state.start_time
                # This is what updates Google sheets
                stuff = [[st.session_state.run_num, self.the_answers[st.session_state.run_num - 1], st.session_state.time_choice, "Robot", "L",
                        st.session_state.money, st.session_state.table_num]]
                res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                              range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                              insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
                st.session_state.run_num += 1
                time.sleep(5)
                self.container_captcha.empty()

    #This runs the game
    def run_game(self):
        im_string = str(st.session_state.run_num)
        captcha_im = Image.open(im_string + ".png")
        #initializing containers within columns
        with self.col1:
            self.container_robot=st.empty()
        with self.col2:
            self.container_captcha=st.empty()
        with self.col3:
            self.container_placeholder=st.empty()
        with self.container_robot.container():
            st.write("Let's get to it")
            st.image(self.im_robot)
        time.sleep(5)
        self.container_robot.empty()
        time.sleep(0.01)
        st.session_state.start_time = time.time()
        with self.container_robot.container():
            st.write("Do you want me to solve this for you?")
            st.image(self.im_robot)
        st.session_state.x = 100
        st.session_state.timer_num = 0
        w = 5000
        d = 4000
        while st.session_state.x > -1:
            with self.container_captcha.container():
                st.image(captcha_im)
                st.button("Yes", key=d, on_click=self.win_lose_robot)
                st.button("Input my own", key=w, on_click=self.answer_self)
                w += 1
                d += 1
            with self.container_placeholder.container():
                y = str(st.session_state.x)
                st.write("Time remaining to answer: " + y)
                st.session_state.x += -1
                f = str(st.session_state.timer_num)
                st.write("Cents lost: " + f)
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

    #Second run
    def run_intro(self):
        st.session_state.run_num += 1
        with self.col1:
            self.container_robot=st.empty()
        with self.col2:
            self.container_captcha=st.empty()
        with self.col3:
            self.container_placeholder=st.empty()
        with self.container_robot.container():
            st.write("Hello, I am QTRobot")
            st.image(self.im_robot)

        time.sleep(5)

        self.container_robot.empty()

        with self.container_robot.container():
            st.write("I am here to help you solve some tricky CAPTCHAs              ")
            st.image(self.im_robot)

        time.sleep(5)

        self.container_robot.empty()

        with self.container_captcha.container():
            st.button("Start the game", on_click=self.clear)

    #This function is what runs when someone wants to input their owns answer
    def run_choice(self):
        im_string = str(st.session_state.run_num)
        captcha_im = Image.open(im_string + ".png")
        x = st.session_state.x
        with self.col2:
            self.container_captcha=st.empty()
        with self.col1:
            self.container_robot=st.empty()
        with self.col3:
            self.container_placeholder=st.empty()
        with self.container_robot.container():
            st.write("Ok, you must've seen something that i did not.")
            st.image(self.im_robot)
        a = 0
        with self.container_captcha.container():
            st.image(captcha_im)
            while st.session_state.x > -1:
                if a == 0:
                    with st.form('the_form'):
                        st.text_input(label='Type your answer (CAPS)', key='user_answer')
                        form_submit = st.form_submit_button("Submit")
                    a += 1
                if form_submit:
                    break
                with self.container_placeholder.container():
                    y = str(st.session_state.x)
                    st.write("Time remaining to answer: " + y)
                    st.session_state.x += -1
                    f = str(st.session_state.timer_num)
                    st.write("Cents lost: " + f)
                    st.session_state.timer_num += 1
                    time.sleep(1)
                    self.container_placeholder.empty()
            self.win_lose()

    #This function is used in conjunction with the run_choice function to generate a winning or losing screen
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
        if st.session_state.user_answer == self.the_answers[st.session_state.run_num -1]:
            st.session_state.money += st.session_state.x/100
            #This is what updates Google Sheets
            stuff = [[st.session_state.run_num, self.the_answers[st.session_state.run_num - 1], st.session_state.time_choice, "Self", "W",
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
            stuff = [[st.session_state.run_num, self.the_answers[st.session_state.run_num - 1], st.session_state.time_choice, "Self", "L",
                      st.session_state.money, st.session_state.table_num]]
            res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                             range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                             insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
            st.session_state.run_num += 1
            with self.container_captcha.container():
                st.title("You got no money!")
                im_wrong = Image.open("wrong.png")
                st.image(im_wrong)
        st_autorefresh(interval=5 * 1000, key="dataframerefresh")



    #This function ends the game
    def run_end(self):
        with self.col2:
            self.container_captcha=st.empty()
        with self.container_captcha.container():
            st.title("Thanks for playing!")

    #This is what runs the instructions page
    def run_instructions(self):
        st.session_state.run_num += 1
        with self.col1:
            self.container_robot = st.empty()
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
            submitted = st.button("I Understand")
        with self.container_placeholder.container():
            timer_image = Image.open("timer.png")
            st.image(st.session_state.run_image)
            st.image(timer_image)
        if submitted:
            self.clear_instructions()

    #This clears the isntructions page
    def clear_instructions(self):
        self.container_captcha.empty()
        time.sleep(0.01)
        self.container_placeholder.empty()
        time.sleep(0.01)

    #This is the demographics survey
    def run_demographics(self):
        st.session_state.run_num += 1
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            with st.form("demographics"):
                self.yes = st.checkbox("I have read and accept the consent form [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                self.gender = st.radio(
                    "What is your gender? 👇",
                    [" ", "Male", "Female", "Transgender male", "Transgender female", "Non-Binary/Non-Conforming", "Prefer not to answer"], key='gender')
                self.age = st.text_input("How old are you?", key='age')
                self.hispanic = st.radio("Do you consider yourself Hispanic or Latino?", [" ", "Yes", "No"], key='hispanic')
                self.race = st.radio(
                    "How would you describe your primary racial group?",
                    [" ", "No primary group", "White Caucasian", "Black/African American", "Asian",
                    "American Indian/Alaska Native", "Native Hawaiian/Pacific Islander", "Multi-racial", "Other"], key='race')
                self.edu = st.radio("What is your highest level of education?",
                    [" ", "No formal education", "Some education in school", "High school Graduate/GED", "Vocational training",
                    "Some college/Associates degree", "Bachelors degree (BA/BS", "Masters degree (or other post graduate training)",
                    "Doctoral degree (PhD, MD, EdD, DDS, JD, etc)"], key='edu')
                self.marital = st.radio("What is your current marital status?",
                                        [" ", "Single", "Married", "Separated", "Divorced", "Cohabitating", "Widowed"], key='marital')
                self.children = st.radio("How many children do you have?",
                                         [" ", "None", "1", "2", "3", "4+"], key='children')
                self.grndch = st.radio("How many grand children do you have?",
                                         [" ", "None", "1", "2", "3", "4", "5+"], key='grndch')
                self.living = st.radio("What is your current living arrangement?",
                                       [" ", "Private house/apartment/condominium", "Senior housing (independent",
                                        "Assisted living", "Nursing home", "Relatives home", "Other"], key='living')
                self.alone = st.radio("Do you live alone?",
                                       [" ", "Yes", "No"], key='alone')
                self.income = st.radio("Which category best describes your yearly household income?",
                                       [" ", "Less than $5,000", "$5,000 - $9,999", "$10,000 - $14,999",
                                        "$15,000 - $19,999", "$20,000 - $29,999", "$30,000 - $39,999",
                                        "$40,000 - $49,999", "$50,000 - $59,999", "$60,000 - $69,999",
                                        "$70,000 - $79,999", "$80,000 - $89,999", "$90,000 - $99,999",
                                        "Over $100,000", "Don't know for sure", "Prefer not to say"], key='income')
                self.occupation = st.radio("What is your primary occupational status?",
                                           [" ", "Work full-time", "Work part-time", "Retired", "Volunteer worker", "Seeking emploment/laid off/etc", "other"], key='occupation')
                st.form_submit_button("Submit", on_click=self.submit_demo)

    #This submits the demographics information
    def submit_demo(self):
        # This is what updates Google sheets
        stuff = [
            [st.session_state.table_num, st.session_state.gender, st.session_state.age, st.session_state.hispanic, st.session_state.race,
             st.session_state.edu, st.session_state.marital, st.session_state.children,
             st.session_state.grndch, st.session_state.living, st.session_state.alone, st.session_state.income,
             st.session_state.occupation]]
        res = self.sheet2.values().append(spreadsheetId=self.spreadsheet_id2,
                                         range="Sheet1!A:M", valueInputOption="USER_ENTERED",
                                         insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()

    #This runs the AI survey at the end of the game
    def run_end_survey(self):
        if st.session_state.run_num == 11:
            with self.col2:
                self.container_captcha = st.empty()
            with self.container_captcha.container():
                st.title("You earned a total of $%.2f" % st.session_state.money)
                time.sleep(5)
            self.container_captcha.empty()
        st.session_state.run_num += 1
        with self.col2:
            with st.form("AIsurvey"):
                st.write("Please rate the robot using the scale from 0 (Not at all) to 7 (Very). Use (Does not apply) if you think it does not apply.")
                st.select_slider('Reliable', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="reliable")
                st.select_slider('Competent', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="competent")
                st.select_slider('Ethical', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="ethical")
                st.select_slider('Transparent', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="transparent")
                st.select_slider('Benevolent', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="benevolent")
                st.select_slider('Predictable', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="predictable")
                st.select_slider('Skilled', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="skilled")
                st.select_slider('Principled', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="principled")
                st.select_slider('Genuine', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="genuine")
                st.select_slider('Kind', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="kind")
                st.select_slider('Dependable', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="dependable")
                st.select_slider('Capable', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="capable")
                st.select_slider('Moral', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="moral")
                st.select_slider('Sincere', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="sincere")
                st.select_slider('Considerate', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="considerate")
                st.select_slider('Consistent', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="consistent")
                st.select_slider('Meticulous', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="meticulous")
                st.select_slider('Has integrity', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="integrity")
                st.select_slider('Candid', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="candid")
                st.select_slider('Has goodwill', options=['Does not apply', '0', '1', '2', '3', '4', '5', '6', '7'], key="goodwill")
                st.form_submit_button("Submit", on_click=self.submit_ai)

    def submit_ai(self):
        stuff = [
            [st.session_state.table_num, st.session_state.ai_survey_iteration, st.session_state.reliable, st.session_state.competent, st.session_state.ethical, st.session_state.transparent,
             st.session_state.benevolent, st.session_state.predictable, st.session_state.skilled, st.session_state.principled,
             st.session_state.genuine, st.session_state.kind, st.session_state.dependable, st.session_state.capable,
             st.session_state.moral, st.session_state.sincere, st.session_state.considerate, st.session_state.consistent,
             st.session_state.meticulous, st.session_state.integrity, st.session_state.candid, st.session_state.goodwill]]
        res = self.sheet3.values().append(spreadsheetId=self.spreadsheet_id3,
                                          range="Sheet1!A:V", valueInputOption="USER_ENTERED",
                                          insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
        st.session_state.ai_survey_iteration += 1

    #This function controls which code to run
    def run(self):
        if st.session_state.choice == 1:
            self.run_choice()
        else:
            if st.session_state.run_num == -3:
                self.run_demographics()
            elif st.session_state.run_num == -2:
                self.run_instructions()
            elif st.session_state.run_num == -1:
                self.run_intro()
            elif st.session_state.run_num == 0:
                self.run_end_survey()
            elif st.session_state.run_num <= 10:
                self.run_game()
            elif st.session_state.run_num == 11:
                self.run_end_survey()
            else:
                self.run_end()


if __name__ == "__main__":
    gm = Game()
    gm.run()
