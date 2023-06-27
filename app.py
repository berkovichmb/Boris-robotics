# A script to create image captcha game
import streamlit as st
import random
import time
from captcha.image import ImageCaptcha
from PIL import Image

class Game:
    def __init__(self):
        #initializes columns and answer variable
        self.col1, self.col2, self.col3 = st.columns((1, 3, 1))
        self.answer = ""

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


    #prints captcha image
    def Captcha_print(self):
        captcha_string = self.random_text()
        image = ImageCaptcha(width = 280, height = 90)
        data = image.generate(captcha_string)
        img = image.write(captcha_string, (captcha_string) + ".png")
        im_captcha = Image.open(captcha_string + ".png")
        st.image(im_captcha)

    #returns random text for captcha to print
    def random_text(self):
        length = 8
        random_str = ''.join((random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(length)))
        self.answer = random_str
        return random_str

    #waits an inputted amount of time
    def wait(self, amount):
        f = 0
        while f < amount:
            time.sleep(1)
            f += 1


    def run_one(self):
        f = 0

        #First iteration
        with self.col1:
            container_robot = st.empty()
            with container_robot.container():
                st.write("I am here to help you solve this Captcha")
                im_robot = Image.open("qtrobot.jpeg")
                st.image(im_robot)

        with self.col3:
            container_lady = st.empty()
            with container_lady.container():
                st.write("Thank you, they're very hard to read    ")
                im_lady = Image.open("oldlady.jpg")
                st.image(im_lady)

        self.wait(5)

        container_robot.empty()
        container_lady.empty()

        with self.col1:
            container_robot = st.empty()
            with container_robot.container():
                st.write("This Captcha is tricky                  ")
                im_robot = Image.open("qtrobot.jpeg")
                st.image(im_robot)

        with self.col2:
            container_captcha = st.empty()
            with container_captcha.container():
                self.Captcha_print()

        with self.col3:
            container_lady = st.empty()
            with container_lady.container():
                st.write("I certainly can't read it               ")
                im_lady = Image.open("oldlady.jpg")
                st.image(im_lady)

        self.wait(5)

        container_robot.empty()
        container_lady.empty()
        container_captcha.empty()

        with self.col1:
            container_robot = st.empty()
            with container_robot.container():
                st.write("The answer is " + self.answer + "          ")
                im_robot = Image.open("qtrobot.jpeg")
                st.image(im_robot)

        with self.col2:
            with container_captcha.container():
                st.button("abcdefgh")
                st.button(self.answer)
                st.button("lmnopqrs")

        with self.col3:
            container_lady = st.empty()
            with container_lady.container():
                st.write("You seem like a smart robot    ")
                im_lady = Image.open("oldlady.jpg")
                st.image(im_lady)

    def run(self):
        if st.session_state.run_num == 1:
            self.run_one()
            

if __name__ == "__main__":
    gm = Game()
    gm.run()
