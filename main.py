from kivymd.app import MDApp
from kivy.lang import Builder
from kivy_lang.kivy_lang import KV
import pyrebase

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
    # firebase_url = "https://easyshopping-8e66f-default-rtdb.europe-west1.firebasedatabase.app/.json"
    currently_logged_in_token = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

    def sign_up(self):
        try:
            auth.create_user_with_email_and_password(self.root.ids.user_email.text, self.root.ids.user_password.text)
        except Exception:
            print("E-Mail already used!")
            # TODO

    def login(self):
        try:
            login = auth.sign_in_with_email_and_password(self.root.ids.user_email.text,
                                                         self.root.ids.user_password.text)
            self.currently_logged_in_token = login["idToken"]
            self.currently_logged_in_token = auth.refresh(login["refreshToken"])
        except Exception:
            print("Invalid E-Mail or Password")
            # TODO

    def forgotten_password(self):
        pass
        # TODO

    def join_as_guest(self):
        login = auth.sign_in_anonymous()
        self.currently_logged_in_token = login["idToken"]
        self.currently_logged_in_token = auth.refresh(login["refreshToken"])


if __name__ == '__main__':
    EasyShopping().run()
