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
        # This hides the menu drop down
        hide_menu_style = """
                       <style>
                       #MainMenu {visibility: hidden;}
                       </style>
                       """
        st.markdown(hide_menu_style, unsafe_allow_html=True)
        # Initializing the Google sheets connection for the data and demographics survey
        self.spreadsheet_id3 = '1kgzVWlDqGQu68xU5cJ6gPvDMHIaV5ZwpAw2WdvGHzgo'
        self.spreadsheet_id2 = '1WFr2iE8cxSBUOmq00rnoNEG84j2jXp1vHxExznZ7VX0'
        self.spreadsheet_id1 = '1XDYHfCOPz7s9etxCGA9p3JBafXsWulkwa90O8OjEtz4'
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

        # initializes state variable to keep track of amount of runs game has gone
        if 'the_answers' not in st.session_state:
            st.session_state.the_answers = ["73VhYgyAV9", "bhp3Le", "Na3dmb", "q9Hspcsz6k", "ywZX6YC2", "kYQf27", "mpUUknUe",
                   "MzWcyippPq", "gfiYcgzuGp", "e7urd9"]

        if 'im_robot' not in st.session_state:
            st.session_state.im_robot = Image.open("qtrobot.png")

        if 'im_robot_heart' not in st.session_state:
            st.session_state.im_robot_heart = Image.open("qtrobot_heart.png")

        if 'im_money' not in st.session_state:
            st.session_state.im_money = Image.open("money.png")

        if 'im_wrong' not in st.session_state:
            st.session_state.im_wrong = Image.open("wrong.png")

        if 'run_num' not in st.session_state:
            st.session_state.run_num = -4

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

        if 'gender' not in st.session_state:
            st.session_state.gender = " "

        if 'age' not in st.session_state:
            st.session_state.age = ""

        if 'hispanic' not in st.session_state:
            st.session_state.hispanic = ""

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

        if 'check' not in st.session_state:
            st.session_state.check = 'Does not apply'

        if 'ai_survey_iteration' not in st.session_state:
            st.session_state.ai_survey_iteration = 1

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
        robot_answer = str(st.session_state.the_answers[st.session_state.run_num - 1])
        with self.col1:
            self.container_robot = st.empty()
        with self.col2:
            self.container_captcha = st.empty()
        if st.session_state.out_of_time == 1:
            st.session_state.out_of_time = 0
            stuff = [
                [st.session_state.run_num, st.session_state.the_answers[st.session_state.run_num - 1], 100,
                 "Out of time", "L",
                 st.session_state.money, st.session_state.table_num]]
            res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                              range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                              insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
            st.session_state.run_num += 1
            with self.container_captcha.container():
                st.title("You got no money!")
                st.image(st.session_state.im_wrong)
                st.session_state.to_continue = 1
                st.button("Play again", on_click=self.clear)
        else:
            with self.container_robot.container():
                st.write("I believe the answer is " + robot_answer + ", ill submit it for you.")
                st.image(st.session_state.im_robot_heart)
            time.sleep(5)
            self.container_robot.empty()
            time.sleep(0.01)
            the_amount = str(st.session_state.x / 100)
            if robot_answer == st.session_state.the_answers[st.session_state.run_num - 1]:
                st.session_state.money += st.session_state.x / 100
                # This is what updates Google sheets
                stuff = [[st.session_state.run_num, st.session_state.the_answers[st.session_state.run_num - 1],
                          st.session_state.time_choice, "Robot", "W", st.session_state.money,
                          st.session_state.table_num]]
                res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                                  range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                                  insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
                st.session_state.run_num += 1
                with self.container_captcha.container():
                    st.title("You got $" + the_amount)
                    st.image(st.session_state.im_money)
                    st.session_state.to_continue = 1
                    st.button("Play again", on_click=self.clear)
            elif robot_answer != st.session_state.the_answers[st.session_state.run_num - 1]:
                # This is what updates Google sheets
                stuff = [[st.session_state.run_num, st.session_state.the_answers[st.session_state.run_num - 1],
                          st.session_state.time_choice, "Robot", "L",
                          st.session_state.money, st.session_state.table_num]]
                res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                                  range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                                  insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
                st.session_state.run_num += 1
                with self.container_captcha.container():
                    st.title("You got no money!")
                    st.image(st.session_state.im_wrong)
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
            st.image(st.session_state.im_robot)
        with self.container_captcha.container():
            st.button("Continue", on_click=self.clear)

    def run_round_survey(self):
        st.session_state.round_survey = 0
        with self.col1:
            self.container_robot = st.empty()
        with self.col2:
            self.container_survey = st.empty()
        with self.container_robot.container():
            st.image(st.session_state.im_robot)
        with self.container_survey.container():
            with st.form("my_form"):
                st.slider("Did you trust that the robot knew the answer? (1 = Did not trust, 7 = Trusted completely)", 1, 7, key='knew_answer')
                st.slider("How would you rate the competence of the robot? (1 = Very incompetent, 7 = Very competent)", 1, 7, key='competence')
                st.slider("How would you describe the robot? (1 = Cold, 7 = Warm)", 1, 7, key='describe')
                st.form_submit_button("Submit", on_click=self.round_survey_submit)

    def round_survey_submit(self):
        self.container_survey.empty()
        spreadsheet_id4 = '19dRHX2Ne9ip-uYs502Mt6FGFWFpVIH7bRGWNajYxXKI'
        time.sleep(0.01)
        stuff = [[st.session_state.table_num, st.session_state.run_num, st.session_state.knew_answer, st.session_state.competence,
                      st.session_state.describe]]
        res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                              range="Sheet1!I:M", valueInputOption="USER_ENTERED",
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
            st.image(st.session_state.im_robot)
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
            st.image(st.session_state.im_robot)
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
            st.image(st.session_state.im_robot)
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
        if st.session_state.user_answer == st.session_state.the_answers[st.session_state.run_num - 1]:
            st.session_state.money += st.session_state.x / 100
            # This is what updates Google Sheets
            stuff = [
                [st.session_state.run_num, st.session_state.the_answers[st.session_state.run_num - 1], st.session_state.time_choice,
                 "Self", "W",
                 st.session_state.money, st.session_state.table_num]]
            res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                              range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                              insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
            the_amount = str(st.session_state.x / 100)
            with self.container_captcha.container():
                st.title("You got $" + the_amount)
                st.image(st.session_state.im_money)
                st.session_state.run_num += 1
        else:
            stuff = [
                [st.session_state.run_num, st.session_state.the_answers[st.session_state.run_num - 1], st.session_state.time_choice,
                 "Self", "L",
                 st.session_state.money, st.session_state.table_num]]
            res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                              range="Sheet1!A:G", valueInputOption="USER_ENTERED",
                                              insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
            st.session_state.run_num += 1
            with self.container_captcha.container():
                st.title("You got no money!")
                st.image(st.session_state.im_wrong)
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
            st.title("Thanks for playing!")


    # This is what runs the instructions page
    def run_instructions(self):
        st.session_state.run_num += 1
        with self.col1:
            self.container_robot = st.empty()
        with self.col2:
            self.container_captcha = st.empty()
        with self.col3:
            self.container_placeholder = st.empty()
        with self.container_robot:
            st.image(st.session_state.im_robot)
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
        self.container_robot.empty()
        time.sleep(0.01)
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

            st.markdown(">Study Title: Older adults trusting AI.  "
                        "\nFunding source: The National Science Foundation (NSF) is funding this research study."
                        "  \n  \nResearcher[s]: Paul Robinette, Electrical and Computer engineering professor; Russell Perkins, PhD candidate; Boris Berkovich, Bachelor's candidate, EECE"
                        "  \n  \nWe’re inviting you to participate in a research study. Participation is completely voluntary. If you agree to participate, you can always change your mind and withdraw. There are no negative consequences, whatever you decide."
                        "  \n  \nWhat is the purpose of this study?"
                        "  \nThis project investigates how trust in AI affects human decision making. AI is getting increasingly complex and it is important to understand how human trust in AI will affect how humans respond to AI."
                        "  \n  \nWhat will i do and how long will it take?"
                        "  \nThis experiment will take anywhere between 10 and 30 minutes based on your response time. During the game you will have to complete 2 surveys, play the game, then complete another survey at the end."
                        "  \nWe will record your survey responses and actions during the game. The surveys will include questions about your demographics and how you would attribute a value to a robot"
                        "  \nIf you participate in this study with a physical robot, you will be video recorded to allow the robot to monitor  your non-verbal cues for emotional indicators. These recordings will be used for documentation in publications and presentations and are crucial for the research. If you do not wish to be recorded, please do not participate in the study."
                        "  \n  \nCould being in this research hurt me?"
                        "  \nSome questions may be personal. You can skip questions you don't want to answer or stop the research at any time."
                        "  \nThere is a chance that your data could be seen by someone who shouldn't have access to it. Were minimizing this risk in the following way:"
                        "  \nAll identifying information is kept separately from research data, but we will be able to link it to you."
                        "  \n  \nWill being in this research help me in any way?"
                        "  \nThere are no direct benefits to you."
                        "  \n  \nHow many people will take part in this research?"
                        "  \nThere are a maximum number # participants including yourself."
                        "  \n  \nWill it cost me any money to participate in this research?"
                        "  \nNone"
                        "  \n  \nWill i receive any compensation for participating in the study?"
                        "  \nYou will be given a $# gift card upon completing the experiment."
                        "  \n  \nHow and where will my information be stored and when will it be destroyed?"
                        "  \nYour information will be stored on the researchers’ encrypted, password protected computers and external hard drives. The data will be kept for up to 5 years after the close of the study. Any released, anonymized data (i.e. publications or datasets) may be kept indefinitely."
                        "  \nIt is possible that we might use the research data in other future research. We may also share data with researchers and companies that are not part of UML. In these cases, we will not share your name or other information that identifies you directly, and we will not come back to you to ask you for your consent."
                        "  \n  \nWho can see my data?"
                        "  \nWe (the researchers) will have access to all collected data (i.e., survey responses, audio files, videos and photos) associated with your anonymized alphanumeric code. This is so we can analyze the data and conduct the study."
                        "  \n•	The Institutional Review Board (IRB) at UML, the Office for Human Research Protections (OHRP), the National Science Foundation (NSF) may review all the study data. This is to ensure we’re following laws and ethical guidelines."
                        "  \n•	We may share our findings in publications or presentations. If we do, the results will de-identified (no names, birthdate, address, etc.). If we quote you, we’ll use pseudonyms (fake names)."
                        "  \n•	Researchers in the AI-Carning consortium, which is the NSF funded project that our research falls under, may also have access to this data. Sharing of data with other researchers will only be done in such a manner that you will not be identified."
                        "  \n  \nContact Information:"
                        "  \nFor questions about the research, complaints, or problems: Contact Paul Robinette, 978-934-3347, paul_robinette@uml.edu"
                        "  \n  \nFor questions about your rights as a research participant, complaints, or problems: Contact the UMass Lowell IRB (Institutional Review Board) at 978-934-4134 or at IRB@uml.edu "
                        "  \n  \nAgreement to Participate:"
                        "  \n I confirm I am volunteering freely to participate in this research project. I have read and fully understand the purpose of the research project and its risks and benefits. I have had the opportunity to read this document and discuss my concerns and questions. I consent to participate in this research."
                        )
            st.button("I agree", on_click=self.clear)
            st.button("I disagree", on_click=self.disagree)

    def disagree(self):
        self.container_captcha.empty()
        time.sleep(0.01)
        with self.container_captcha:
            st.write("Close this screen")
        st.session_state.run_num = -1000
        time.sleep(10000)

    def run_demographics(self):
        st.session_state.run_num += 1
        with self.col1:
            self.container_robot = st.empty()
        with self.container_robot.container():
            st.image(st.session_state.im_robot)
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha:
            with st.form("demographics"):
                st.radio(
                    "What is your gender? 👇",
                    [" ", "Male", "Female", "Transgender male", "Transgender female", "Non-Binary/Non-Conforming",
                     "Prefer not to answer"], key='gender')
                st.text_input("How old are you?", key='age')
                st.radio("Do you consider yourself Hispanic or Latino?", [" ", "Yes", "No"], key='hispanic')
                st.radio(
                    "How would you describe your primary racial group?",
                    [" ", "No primary group", "White Caucasian", "Black/African American", "Asian",
                     "American Indian/Alaska Native", "Native Hawaiian/Pacific Islander", "Multi-racial", "Other"],
                    key='race')
                st.radio("What is your highest level of education?",
                         [" ", "No formal education", "Some education in school", "High school Graduate/GED",
                          "Vocational training",
                          "Some college/Associates degree", "Bachelors degree (BA/BS",
                          "Masters degree (or other post graduate training)",
                          "Doctoral degree (PhD, MD, EdD, DDS, JD, etc)"], key='edu')
                st.radio("What is your current marital status?",
                         [" ", "Single", "Married", "Separated", "Divorced", "Cohabitating", "Widowed"],
                         key='marital')
                st.radio("How many children do you have?",
                         [" ", "None", "1", "2", "3", "4+"], key='children')
                st.radio("How many grand children do you have?",
                         [" ", "None", "1", "2", "3", "4", "5+"], key='grndch')
                st.radio("What is your current living arrangement?",
                         [" ", "Private house/apartment/condominium", "Senior housing (independent",
                          "Assisted living", "Nursing home", "Relatives home", "Other"], key='living')
                st.radio("Do you live alone?",
                         [" ", "Yes", "No"], key='alone')
                st.radio("Which category best describes your yearly household income?",
                         [" ", "Less than $5,000", "$5,000 - $9,999", "$10,000 - $14,999",
                          "$15,000 - $19,999", "$20,000 - $29,999", "$30,000 - $39,999",
                          "$40,000 - $49,999", "$50,000 - $59,999", "$60,000 - $69,999",
                          "$70,000 - $79,999", "$80,000 - $89,999", "$90,000 - $99,999",
                          "Over $100,000", "Don't know for sure", "Prefer not to say"], key='income')
                st.radio("What is your primary occupational status?",
                         [" ", "Work full-time", "Work part-time", "Retired", "Volunteer worker",
                          "Seeking emploment/laid off/etc", "other"], key='occupation')
                st.form_submit_button("Submit", on_click=self.submit_demo)

    def submit_demo(self):
        # This is what updates Google sheets
        stuff = [
                [st.session_state.table_num, st.session_state.gender, st.session_state.age, st.session_state.hispanic,
                 st.session_state.race,
                 st.session_state.edu, st.session_state.marital, st.session_state.children,
                 st.session_state.grndch, st.session_state.living, st.session_state.alone, st.session_state.income,
                 st.session_state.occupation]]
        res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                              range="Sheet1!O:AA", valueInputOption="USER_ENTERED",
                                              insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()

    def run_end_survey1(self):
        st.session_state.to_continue = 1
        st.session_state.run_num += 1
        with self.col1:
            self.container_robot = st.empty()
        with self.container_robot.container():
            st.image(st.session_state.im_robot)
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            with st.form("AIsurvey"):
                st.write("Please rate the robot using the scale from 1 (Not at all) to 7 (Very). Use (Does not apply) if you think it does not apply.")
                st.select_slider('Reliable', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="reliable")
                st.select_slider('Competent', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="competent")
                st.select_slider('Ethical', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="ethical")
                st.select_slider('Transparent', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="transparent")
                st.select_slider('Benevolent', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="benevolent")
                st.select_slider('Predictable', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="predictable")
                st.select_slider('Skilled', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="skilled")
                st.select_slider('Principled', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="principled")
                st.select_slider('Genuine', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="genuine")
                st.select_slider('Kind', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="kind")
                st.select_slider('Dependable', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="dependable")
                st.select_slider('Capable', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="capable")
                st.select_slider('Moral', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="moral")
                st.select_slider('Sincere', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="sincere")
                st.select_slider('Considerate', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="considerate")
                st.select_slider('Consistent', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="consistent")
                st.select_slider('Meticulous', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="meticulous")
                st.select_slider('Has integrity', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="integrity")
                st.select_slider('Select 3', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="check")
                st.select_slider('Candid', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="candid")
                st.select_slider('Has goodwill', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="goodwill")
                st.form_submit_button("Submit", on_click=self.submit_ai)


    def run_end_survey2(self):
        st.session_state.run_num += 1
        with self.col1:
            self.container_robot = st.empty()
        with self.container_robot.container():
            st.image(st.session_state.im_robot)
        with self.col2:
            self.container_captcha = st.empty()
        with self.container_captcha.container():
            with st.form("AIsurvey"):
                st.write("Please rate the robot using the scale from 1 (Not at all) to 7 (Very). Use (Does not apply) if you think it does not apply.")
                st.select_slider('Reliable', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="reliable")
                st.select_slider('Competent', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="competent")
                st.select_slider('Ethical', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="ethical")
                st.select_slider('Transparent', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="transparent")
                st.select_slider('Benevolent', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="benevolent")
                st.select_slider('Predictable', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="predictable")
                st.select_slider('Skilled', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="skilled")
                st.select_slider('Principled', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="principled")
                st.select_slider('Genuine', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="genuine")
                st.select_slider('Kind', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="kind")
                st.select_slider('Dependable', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="dependable")
                st.select_slider('Capable', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="capable")
                st.select_slider('Select 7', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="check")
                st.select_slider('Moral', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="moral")
                st.select_slider('Sincere', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="sincere")
                st.select_slider('Considerate', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="considerate")
                st.select_slider('Consistent', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="consistent")
                st.select_slider('Meticulous', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="meticulous")
                st.select_slider('Has integrity', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="integrity")
                st.select_slider('Candid', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'], key="candid")
                st.select_slider('Has goodwill', options=['Does not apply', '1', '2', '3', '4', '5', '6', '7'],key="goodwill")
                st.form_submit_button("Submit", on_click=self.submit_ai)

    def submit_ai(self):
        self.container_captcha.empty()
        stuff = [
            [st.session_state.table_num, st.session_state.ai_survey_iteration, st.session_state.check,
             st.session_state.reliable, st.session_state.competent, st.session_state.ethical,
             st.session_state.transparent,
             st.session_state.benevolent, st.session_state.predictable, st.session_state.skilled,
             st.session_state.principled,
             st.session_state.genuine, st.session_state.kind, st.session_state.dependable, st.session_state.capable,
             st.session_state.moral, st.session_state.sincere, st.session_state.considerate,
             st.session_state.consistent,
             st.session_state.meticulous, st.session_state.integrity, st.session_state.candid,
             st.session_state.goodwill]]
        res = self.sheet1.values().append(spreadsheetId=self.spreadsheet_id1,
                                          range="Sheet1!AC:AY", valueInputOption="USER_ENTERED",
                                          insertDataOption="INSERT_ROWS", body={"values": stuff}).execute()
        st.session_state.ai_survey_iteration += 1

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
            if st.session_state.run_num == -4:
                self.run_consent()
            elif st.session_state.run_num == -3:
                self.run_demographics()
            elif st.session_state.run_num == -2:
                self.run_instructions()
            elif st.session_state.run_num == -1:
                self.run_intro()
            elif st.session_state.run_num == 0:
                self.run_end_survey1()
            elif st.session_state.run_num <= 10:
                self.run_game()
            elif st.session_state.run_num == 11:
                self.run_end_survey2()
            elif st.session_state.run_num == 12:
                self.run_end()

if __name__ == "__main__":
    gc.collect()
    gm = Game()
    gm.run()
