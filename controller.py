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
        self.storage = self.firebase.storage()
        self.currently_logged_in_token = None
        self.currently_logged_in_email = None

    def sign_up(self, email, password, password_again):
        app = App.get_running_app()
        if email == "" or password == "" or password_again == "" or app.dob is None:
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
            app.open_success_dialog("Sikeres regisztráció, most már bejelentkezhetsz!")
        except Exception:
            app.open_error_dialog("Már létezik ilyen Email cím!")

    def login(self, email, password):
        app = App.get_running_app()
        try:
            login = self.auth.sign_in_with_email_and_password(email, password)
            self.currently_logged_in_token = login["idToken"]
            self.currently_logged_in_token = self.auth.refresh(login["refreshToken"])
            self.currently_logged_in_email = email.split(".")[0]
            app.upload_shops()
            app.go_to_nav_screen()
            app.upload_shopping_list()
            app.refresh_favorites()
            print(self.currently_logged_in_token)
            print(self.auth.current_user)
        except Exception:
            app.open_error_dialog("Nem megfelelő felhasználónév vagy jelszó!")

    def join_as_guest(self):
        app = App.get_running_app()
        """login = self.auth.sign_in_anonymous()
        self.currently_logged_in_token = login["idToken"]
        self.currently_logged_in_token = self.auth.refresh(login["refreshToken"])
        app.upload_shops()
        app.go_to_nav_screen()
        app.go_to_home_screen()
        print(self.auth.current_user)"""
        app.upload_shops()
        app.go_to_nav_screen()
        app.go_to_home_screen()

    def log_out(self):
        app = App.get_running_app()
        if self.auth.current_user is not None:
            self.auth.current_user = None
            self.currently_logged_in_email = None
        app.go_to_login_screen()
        print(self.currently_logged_in_email)
        print(self.currently_logged_in_token)
        print(self.auth.current_user)



