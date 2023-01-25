from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy_lang.kivy_lang import KV
import pyrebase
import datetime

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


class WindowManager(ScreenManager):
    pass


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    pass


class ClickableTextFieldRoundPasswordAgain(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    pass


class LoginScreen(Screen):
    pass


class RegisterScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class EasyShopping(MDApp):
    # firebase_url = "https://easyshopping-8e66f-default-rtdb.europe-west1.firebasedatabase.app/.json"
    dialog = None
    currently_logged_in_token = None
    data = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

    def sign_up(self):
        if self.root.get_screen("register").ids.user_email.text is "" or self.root.get_screen(
                "register").ids.register_pw.text is "" or self.root.get_screen(
                "register").ids.register_pw_again.text is "":
            self.open_error_dialog("Az összes mezőt kötelező kitölteni!")
            return

        if self.root.get_screen("register").ids.register_pw.text != self.root.get_screen(
                "register").ids.register_pw_again.text:
            self.open_error_dialog("A megadott jelszavak nem egyeznek!")
            return
        try:
            auth.create_user_with_email_and_password(self.root.get_screen("register").ids.user_email.text,
                                                     self.root.get_screen("register").ids.register_pw.text)
            self.store_user_data()
            self.go_to_login_screen()
        except Exception:
            # TODO túl rövid jelszó vagy használt email probléma eldöntésének lekezelése
            self.open_error_dialog("Már létezik ilyen Email cím!")

    def login(self):
        try:
            login = auth.sign_in_with_email_and_password(self.root.get_screen("login").ids.user_email.text,
                                                         self.root.get_screen("login").ids.login_pw.text)
            self.currently_logged_in_token = login["idToken"]
            self.currently_logged_in_token = auth.refresh(login["refreshToken"])
            self.go_to_home_screen()
            print("nice")
        except Exception:
            self.open_error_dialog("Nem megfelelő felhasználónév vagy jelszó!")

    def forgotten_password(self):
        pass
        # TODO

    def join_as_guest(self):
        login = auth.sign_in_anonymous()
        self.currently_logged_in_token = login["idToken"]
        self.currently_logged_in_token = auth.refresh(login["refreshToken"])

    def open_error_dialog(self, error_text):
        close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Hiba", text=error_text,
                               size_hint=(0.7, 1), buttons=[close_button])
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def store_user_data(self):
        self.data = {"email": self.root.get_screen("register").ids.user_email.text,
                     "date_of_birth": self.root.get_screen("register").ids.date_of_birth.text,
                     "username": self.root.get_screen("register").ids.username.text,
                     "timestamp": str(datetime.datetime.now())
                     }
        db.child("users").child(self.root.get_screen("register").ids.username.text).set(self.data)

    def go_to_login_screen(self):
        self.root.current = "login"

    def go_to_register_screen(self):
        self.root.current = "register"

    def go_to_home_screen(self):
        self.root.current = "home"


if __name__ == '__main__':
    EasyShopping().run()
