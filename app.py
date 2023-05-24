# A script to create image captcha game
import streamlit as st
import random
import time
from captcha.image import ImageCaptcha
from PIL import Image

class Game:
    def __init__(self):
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
            st.session_state.run_num = 1

        if 'run_image' not in st.session_state:
            st.session_state.run_image = Image.open("base.png")

        if 'choice' not in st.session_state:
            st.session_state.choice = 0

        if 'the_answer' not in st.session_state:
            st.session_state.the_answer = "blank"

        if 'text_input' not in st.session_state:
            st.session_state.text_input = "blank"


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
        st.session_state.choice = 1

    #This clears the container after the prize screen
    def clear(self):
        self.container_captcha.empty()

    #function for winning screen
    def win(self):
        st.session_state.run_num += 1
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
        time.sleep(5)

    #function for losing screen
    def loser(self):
        st.session_state.run_num += 1
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

        r = random.randint(1, 2)
        if r == 1:
            with self.container_robot.container():
                st.write("Do you want me to fill this out for you?")
                st.image(self.im_robot)
            with self.container_captcha.container():
                st.image(st.session_state.run_image)
                submitted = st.button("Yes", on_click=self.win)
                st.button("Input my own", key="1", on_click=self.answer_self)
                if submitted:
                    self.win()
        else:
            rand_answer = self.random_scramble()
            with self.container_robot.container():
                st.write("Do you want me to fill this out for you?")
                st.image(self.im_robot)
            with self.container_captcha.container():
                st.image(st.session_state.run_image)
                submitted = st.button("Yes", on_click=self.loser)
                st.button("Input my own", key="1", on_click=self.answer_self)
                if submitted:
                    self.lose()

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
        if r == 1:
            with self.container_robot.container():
                st.write("Do you want me to fill this out for you?")
                st.image(self.im_robot)
            with self.container_captcha.container():
                st.image(st.session_state.run_image)
                st.button("Yes", on_click=self.win)
                st.button("Input my own", key="1", on_click=self.answer_self)
        else:
            rand_answer = self.random_scramble()
            with self.container_robot.container():
                st.write("Do you want me to fill this out for you?")
                st.image(self.im_robot)
            with self.container_captcha.container():
                st.image(st.session_state.run_image)
                st.button("Yes", on_click=self.loser)
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
        st.session_state.run_num += 1
        st.session_state.choice = 0
        if self.text_input == st.session_state.the_answer:
            with self.container_captcha.container():
                st.title("You got 1$")
                im_money = Image.open("money.png")
                st.image(im_money)
                st.button("Play again")
        else:
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


    #This function controls which code to run
    def run(self):
        if st.session_state.choice == 1:
            self.run_choice()
        else:
            if st.session_state.run_num <= 10:
                if st.session_state.run_num == 1:
                    self.run_one()
                else:
                    self.run_two()
            else:
                self.run_end()


if __name__ == "__main__":
    gm = Game()
    gm.run()
