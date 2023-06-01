# A script to create image captcha game
import streamlit as st
import random
import time
from captcha.image import ImageCaptcha
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build

class Game:
    def __init__(self):
        #This hides the menu drop down
        hide_menu_style = """
                <style>
                #MainMenu {visibility: hidden;}
                </style>
                """
        st.markdown(hide_menu_style, unsafe_allow_html=True)

        #Initializing the Google sheets connection
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )

        self.spreadsheet_id = '1XDYHfCOPz7s9etxCGA9p3JBafXsWulkwa90O8OjEtz4'
        service = build('sheets', 'v4', credentials=creds)
        self.sheet = service.spreadsheets()

        #initializes columns and answer variable
        self.col1, self.col2, self.col3 = st.columns((1, 2, 1))
        self.answer = ""
        self.im_robot = Image.open("qtrobot.jpeg")

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
            st.session_state.run_num = 0

        if 'run_image' not in st.session_state:
            st.session_state.run_image = Image.open("base.png")

        if 'choice' not in st.session_state:
            st.session_state.choice = 0

        if 'the_answer' not in st.session_state:
            st.session_state.the_answer = "blank"

        if 'text_input' not in st.session_state:
            st.session_state.text_input = "blank"

        if 'money' not in st.session_state:
            st.session_state.money = 0

        if 'time_choice' not in st.session_state:
            st.session_state.time_choice = 0

        if 'table_num' not in st.session_state:
            st.session_state.table_num = random.randint(0,999999)

        if 'gender' not in st.session_state:
            st.session_state.gender = "Male"

        if 'age' not in st.session_state:
            st.session_state.age = ""

        if 'hispanic' not in st.session_state:
            st.session_state.hispanic = "Yes"

        if 'race' not in st.session_state:
            st.session_state.race = "No primary group"

        if 'edu' not in st.session_state:
            st.session_state.edu = 'No formal education'

        if 'marital' not in st.session_state:
            st.session_state.marital = 'Single'

        if 'children' not in st.session_state:
            st.session_state.children = 'None'

        if 'grndchldrn' not in st.session_state:
            st.session_state.grndchldrn = 'None'

        if 'living' not in st.session_state:
            st.session_state.living = 'Private house/apartment/condominium'

        if 'alone' not in st.session_state:
            st.session_state.alone = 'Yes'

        if 'income' not in st.session_state:
            st.session_state.income = 'Less than $5,000'

        if 'occupation' not in st.session_state:
            st.session_state.occupation = 'Work full-time'


    #prints captcha image
    def Captcha_print(self):
        captcha_string = self.random_text()
        image = ImageCaptcha(width = 280, height = 90)
        data = image.generate(captcha_string)
        img = image.write(captcha_string, (captcha_string) + ".png")
        st.session_state.run_image = Image.open(captcha_string + ".png")
        st.image(st.session_state.run_image)

    #returns random text for captcha to print
    def random_text(self):
        length = 8
        random_str = ''.join((random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(length)))
        st.session_state.the_answer = random_str
        self.answer = random_str
        return random_str

    #Substitutes a letter of the Captcha answer to give wrong answer
    def random_scramble(self):
        r = random.randint(0,7)
        char = self.answer[r]
        y = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        new = self.answer.replace(char, y)
        return new

    #Prepares next iteration to run the run_choice function
    def answer_self(self):
        self.container_robot.empty()
        self.container_captcha.empty()
        self.end = time.time()
        st.session_state.time_choice = self.end-self.start
        st.session_state.choice = 1

    #This clears the container after the prize screen
    def clear(self):
        self.container_captcha.empty()

    #function for winning screen
    def win(self):
        self.end = time.time()
        self.container_robot.empty()
        time.sleep(0.01)
        self.container_captcha.empty()
        time.sleep(0.01)
        with self.container_robot.container():
            st.write("I believe the answer is " + self.answer + ", ill submit it for you.")
            st.image(self.im_robot)
        time.sleep(5)
        self.container_robot.empty()
        time.sleep(0.01)
        with self.container_captcha.container():
            st.title("You got 1$")
            im_money = Image.open("money.png")
            st.image(im_money)
        st.session_state.money += 1
        st.session_state.time_choice = self.end - self.start

        #This is what updates Google sheets
        stuff = [[st.session_state.run_num, st.session_state.the_answer, st.session_state.time_choice, "Robot", "W", st.session_state.money, st.session_state.table_num]]
        res = self.sheet.values().append(spreadsheetId=self.spreadsheet_id,
                                         range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                         insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
        st.session_state.run_num += 1
        time.sleep(5)

    #function for losing screen
    def loser(self):
        self.end = time.time()
        self.container_robot.empty()
        time.sleep(0.01)
        self.container_captcha.empty()
        time.sleep(0.01)
        with self.container_robot.container():
            st.write("I believe the answer is " + self.random_scramble() + ", ill submit it for you.")
            st.image(self.im_robot)
        time.sleep(5)
        self.container_robot.empty()
        time.sleep(0.01)
        with self.container_captcha.container():
            st.title("You lost 1$")
            im_wrong = Image.open("wrong.png")
            st.image(im_wrong)
        if st.session_state.money > 0:
            st.session_state.money += -1
        st.session_state.time_choice = self.end - self.start

        #This is what updates Google sheets
        stuff = [[st.session_state.run_num, st.session_state.the_answer, st.session_state.time_choice, "Robot", "L", st.session_state.money, st.session_state.table_num]]
        res = self.sheet.values().append(spreadsheetId=self.spreadsheet_id,
                                         range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                         insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
        st.session_state.run_num += 1
        time.sleep(5)

    #first iteration
    def run_one(self):
        #initializing containers within columns
        with self.col1:
            self.container_robot=st.empty()
        with self.col2:
            self.container_captcha=st.empty()
        with self.col3:
            self.container_placeholder=st.empty()

        with self.container_robot.container():
            st.write("I am here to help you solve this Captcha")
            st.image(self.im_robot)

        time.sleep(5)

        self.container_robot.empty()

        with self.container_robot.container():
            st.write("This Captcha is tricky                  ")
            st.image(self.im_robot)

        with self.container_captcha.container():
            self.Captcha_print()

        time.sleep(5)

        self.container_robot.empty()
        self.container_captcha.empty()
        self.start = time.time()

        r = random.randint(1, 2)
        if r == 1:
            with self.container_robot.container():
                st.write("Do you want me to fill this out for you?")
                st.image(self.im_robot)
            with self.container_captcha.container():
                st.image(st.session_state.run_image)
                submitted = st.button("Yes", on_click=self.win)
                st.button("Input my own", key="1", on_click=self.answer_self)
        else:
            rand_answer = self.random_scramble()
            with self.container_robot.container():
                st.write("Do you want me to fill this out for you?")
                st.image(self.im_robot)
            with self.container_captcha.container():
                st.image(st.session_state.run_image)
                submitted = st.button("Yes", on_click=self.loser)
                st.button("Input my own", key="1", on_click=self.answer_self)

    #Second run
    def run_two(self):
        with self.col1:
            self.container_robot=st.empty()
        with self.col2:
            self.container_captcha=st.empty()

        with self.container_robot.container():
            st.write("Lets try this again")
            st.image(self.im_robot)

        time.sleep(5)

        self.container_robot.empty()

        with self.container_robot.container():
            st.write("This Captcha is tricky                  ")
            st.image(self.im_robot)

        with self.container_captcha.container():
            self.Captcha_print()

        time.sleep(5)

        self.container_robot.empty()
        self.container_captcha.empty()

        r = random.randint(1, 2)
        self.start = time.time()

        if r == 1:
            with self.container_robot.container():
                st.write("Do you want me to fill this out for you?")
                st.image(self.im_robot)
            with self.container_captcha.container():
                st.image(st.session_state.run_image)
                submitted = st.button("Yes", on_click=self.win)
                st.button("Input my own", key="1", on_click=self.answer_self)
        else:
            rand_answer = self.random_scramble()
            with self.container_robot.container():
                st.write("Do you want me to fill this out for you?")
                st.image(self.im_robot)
            with self.container_captcha.container():
                st.image(st.session_state.run_image)
                submitted = st.button("Yes", on_click=self.loser)
                st.button("Input my own", key="1", on_click=self.answer_self)

    #This function is what runs when someone wants to input their owns answer
    def run_choice(self):
        with self.col2:
            self.container_captcha=st.empty()
        with self.col1:
            self.container_robot=st.empty()
        with self.container_robot.container():
            st.write("Ok, you must've seen something that i did not.")
            st.image(self.im_robot)
        with self.container_captcha.container():
            st.image(st.session_state.run_image)
            self.text_input = st.text_input(label='Type your answer (CAPS)')
            if self.text_input:
                self.win_lose()



    #This function is used in conjunction with the run_choice function to generate a winning or losing screen
    def win_lose(self):
        self.container_robot.empty()
        time.sleep(0.01)
        st.session_state.choice = 0
        if self.text_input == st.session_state.the_answer:
            st.session_state.money += 1

            #This is what updates Google Sheets
            stuff = [[st.session_state.run_num, st.session_state.the_answer, st.session_state.time_choice, "Self", "W",
                      st.session_state.money, st.session_state.table_num]]
            res = self.sheet.values().append(spreadsheetId=self.spreadsheet_id,
                                             range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                             insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()

            st.session_state.run_num += 1
            with self.container_captcha.container():
                st.title("You got 1$")
                im_money = Image.open("money.png")
                st.image(im_money)
                st.button("Play again")

        else:
            if st.session_state.money > 0:
                st.session_state.money += -1
            stuff = [[st.session_state.run_num, st.session_state.the_answer, st.session_state.time_choice, "Self", "L",
                      st.session_state.money, st.session_state.table_num]]
            res = self.sheet.values().append(spreadsheetId=self.spreadsheet_id,
                                             range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                             insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
            st.session_state.run_num += 1
            with self.container_captcha.container():
                st.title("You lost 1$")
                im_wrong = Image.open("wrong.png")
                st.image(im_wrong)
                st.button("Play again")
        time.sleep(5)

    #This function ends the game
    def run_end(self):
        with self.col2:
            self.container_captcha=st.empty()
        with self.container_captcha.container():
            st.title("Thanks for playing!")

    def run_demographics(self):
        st.session_state.run_num += 1
        with self.col2:
            with st.form("demographics"):
                self.yes = st.checkbox("I have read and accept the consent form [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                self.gender = st.radio(
                    "What is your gender? 👇",
                    ["Male", "Female", "Transgender male", "Transgender female", "Non-Binary/Non-Conforming", "Prefer not to answer"], key='gender')
                self.age = st.text_input("How old are you?", key='age')
                self.hispanic = st.radio("Do you consider yourself Hispanic or Latino?", ["Yes", "No"], key='hispanic')
                self.race = st.radio(
                    "How would you describe your primary racial group?",
                    ["No primary group", "White Caucasian", "Black/African American", "Asian",
                    "American Indian/Alaska Native", "Native Hawaiian/Pacific Islander", "Multi-racial", "Other"], key='race')
                self.edu = st.radio("What is your highest level of education?",
                    ["No formal education", "Some education in school", "High school Graduate/GED", "Vocational training",
                    "Some college/Associates degree", "Bachelors degree (BA/BS", "Masters degree (or other post graduate training)",
                    "Doctoral degree (PhD, MD, EdD, DDS, JD, etc)"], key='edu')
                self.marital = st.radio("What is your current marital status?",
                                        ["Single", "Married", "Separated", "Divorced", "Cohabitating", "Widowed"], key='marital')
                self.children = st.radio("How many children do you have?",
                                         ["None", "1", "2", "3", "4+"], key='children')
                self.grndch = st.radio("How many grand children do you have?",
                                         ["None", "1", "2", "3", "4", "5+"], key='grndch')
                self.living = st.radio("What is your current living arrangement?",
                                       ["Private house/apartment/condominium", "Senior housing (independent",
                                        "Assisted living", "Nursing home", "Relatives home", "Other"], key='living')
                self.alone = st.radio("Do you live alone?",
                                       ["Yes", "No"], key='alone')
                self.income = st.radio("Which category best describes your yearly household income?",
                                       ["Less than $5,000", "$5,000 - $9,999", "$10,000 - $14,999",
                                        "$15,000 - $19,999", "$20,000 - $29,999", "$30,000 - $39,999",
                                        "$40,000 - $49,999", "$50,000 - $59,999", "$60,000 - $69,999",
                                        "$70,000 - $79,999", "$80,000 - $89,999", "$90,000 - $99,999",
                                        "Over $100,000", "Don't know for sure", "Prefer not to say"], key='income')
                self.occupation = st.radio("What is your primary occupational status?",
                                           ["Work full-time", "Work part-time", "Retired", "Volunteer worker", "Seeking emploment/laid off/etc", "other"], key='occupation')
                st.form_submit_button("Submit", on_click=self.submit_demo)

    def submit_demo(self):
        # This is what updates Google sheets
        stuff = [
            [st.session_state.table_num, st.session_state.gender, st.session_state.age, st.session_state.hispanic, st.session_state.race,
             st.session_state.edu, st.session_state.marital, st.session_state.children,
             st.session_state.grndch, st.session_state.living, st.session_state.alone, st.session_state.income,
             st.session_state.occupation]]
        res = self.sheet.values().append(spreadsheetId=self.spreadsheet_id,
                                         range="Sheet1!J:U", valueInputOption="USER_ENTERED",
                                         insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()

    #This function controls which code to run
    def run(self):
        if st.session_state.choice == 1:
            self.run_choice()
        else:
            if st.session_state.run_num == 0:
                self.run_demographics()
            elif st.session_state.run_num <= 10:
                if st.session_state.run_num == 1:
                    self.run_one()
                else:
                    self.run_two()
            else:
                self.run_end()


if __name__ == "__main__":
    gm = Game()
    gm.run()
