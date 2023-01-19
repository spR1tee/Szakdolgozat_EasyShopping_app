from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import pyrebase
import requests
import json

firebase_config = {
    'apiKey': "AIzaSyDCCgo6Iq_Xzrfh1tUJhRh8QTw8T1uhtSo",
    'authDomain': "easyshopping-8e66f.firebaseapp.com",
    'databaseURL': "https://easyshopping-8e66f-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "easyshopping-8e66f",
    'storageBucket': "easyshopping-8e66f.appspot.com",
    'messagingSenderId': "1084432810111",
    'appId': "1:1084432810111:web:a412cda67fce880560bf4a"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()


class EasyShopping(MDApp):
    firebase_url = "https://easyshopping-8e66f-default-rtdb.europe-west1.firebasedatabase.app/.json"
    currently_logged_in_token = None

    def build(self):
        box_layout = BoxLayout()
        button = Button(text="Create")
        box_layout.add_widget(button)
        return box_layout

    def sign_up(self, user_email, user_password):
        try:
            auth.create_user_with_email_and_password(user_email, user_password)
        except Exception:
            print("E-Mail already used!")
            # TODO

    def login(self, user_email, user_password):
        try:
            login = auth.sign_in_with_email_and_password(user_email, user_password)
            self.currently_logged_in_token = login["idToken"]
            self.currently_logged_in_token = auth.refresh(login["refreshToken"])
        except Exception:
            print("Invalid E-Mail or Password")
            # TODO


if __name__ == '__main__':
    EasyShopping().run()
