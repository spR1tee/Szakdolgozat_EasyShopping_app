import pyrebase
from kivy.app import App

firebase_config = {
    'apiKey': "AIzaSyDCCgo6Iq_Xzrfh1tUJhRh8QTw8T1uhtSo",
    'authDomain': "easyshopping-8e66f.firebaseapp.com",
    'databaseURL': "https://easyshopping-8e66f-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "easyshopping-8e66f",
    'storageBucket': "easyshopping-8e66f.appspot.com",
    'messagingSenderId': "1084432810111",
    'appId': "1:1084432810111:web:a412cda67fce880560bf4a"
}


class Controller:
    def __init__(self):
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.currently_logged_in_token = None

    def sign_up(self, email, password, password_again):
        app = App.get_running_app()
        if email is "" or password is "" or password_again is "" or app.dob is None:
            app.open_error_dialog("Az összes mezőt kötelező kitölteni!")
            return

        if password != password_again:
            app.open_error_dialog("A megadott jelszavak nem egyeznek!")
            return

        if len(password) < 6:
            app.open_error_dialog("A jelszónak legalább 6 karakter hosszúnak kell lennie!")
            return

        try:
            self.auth.create_user_with_email_and_password(email, password)
            app.store_user_data()
            app.go_to_login_screen()
        except Exception:
            app.open_error_dialog("Már létezik ilyen Email cím!")

    def login(self):
        pass

    def join_as_guest(self):
        pass
