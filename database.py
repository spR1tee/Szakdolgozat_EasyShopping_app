import datetime

import pyrebase
from kivymd.app import MDApp

firebase_config = {
    'apiKey': "AIzaSyDCCgo6Iq_Xzrfh1tUJhRh8QTw8T1uhtSo",
    'authDomain': "easyshopping-8e66f.firebaseapp.com",
    'databaseURL': "https://easyshopping-8e66f-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "easyshopping-8e66f",
    'storageBucket': "easyshopping-8e66f.appspot.com",
    'messagingSenderId': "1084432810111",
    'appId': "1:1084432810111:web:a412cda67fce880560bf4a"
}


class Database:

    def __init__(self):
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()
        self.currently_logged_in_token = None
        self.currently_logged_in_email = None

    def sign_up(self, email, password, password_again):
        app = MDApp.get_running_app()
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
            self.store_user_data()
            app.go_to_login_screen()
            app.open_success_dialog("Sikeres regisztráció, most már bejelentkezhetsz!")
        except Exception:
            app.open_error_dialog("Már létezik ilyen Email cím!")

    def login(self, email, password):
        app = MDApp.get_running_app()
        try:
            login = self.auth.sign_in_with_email_and_password(email, password)
            self.currently_logged_in_token = login["idToken"]
            self.currently_logged_in_token = self.auth.refresh(login["refreshToken"])
            self.currently_logged_in_email = email.split(".")[0]
            app.upload_shops()
            app.controller.go_to_nav_screen()
            app.upload_shopping_list()
            app.refresh_favorites()
            print(self.currently_logged_in_token)
            print(self.auth.current_user)
        except Exception:
            app.open_error_dialog("Nem megfelelő felhasználónév vagy jelszó!")

    def join_as_guest(self):
        app = MDApp.get_running_app()
        login = self.auth.sign_in_anonymous()
        self.currently_logged_in_token = login["idToken"]
        self.currently_logged_in_token = self.auth.refresh(login["refreshToken"])
        app.upload_shops()
        app.controller.go_to_nav_screen()
        app.controller.go_to_home_screen()
        print(self.auth.current_user)

    def log_out(self):
        app = MDApp.get_running_app()
        if self.auth.current_user is not None:
            self.auth.current_user = None
            self.currently_logged_in_email = None
        app.controller.go_to_login_screen()
        print(self.currently_logged_in_email)
        print(self.currently_logged_in_token)
        print(self.auth.current_user)

    def check_favorites(self):
        all_shops = self.db.child("shops").get()
        in_fav = []
        if self.auth.current_user is not None:
            if "registered" in self.auth.current_user.keys():
                if self.auth.current_user["registered"] is True:
                    favorites = self.db.child("users").child(
                        self.currently_logged_in_email).child(
                        "favorites").get()
                    if favorites.each() is not None and favorites.each() != "":
                        for shop in all_shops.each():
                            for fav in favorites.each():
                                if shop.key() == fav.key():
                                    in_fav.append(shop.key())

        return in_fav

    def check_if_registered(self):
        if self.auth.current_user is not None:
            if "registered" in self.auth.current_user.keys():
                if self.auth.current_user["registered"] is True:
                    return True

        return False

    def get_all_shops(self):
        return self.db.child("shops").get()

    def get_favorites(self):
        favorites = []
        if self.check_if_registered():
            favorites = self.db.child("users").child(
                self.currently_logged_in_email).child(
                "favorites").get()
        return favorites

    def get_shopping_list(self):
        return self.db.child("users").child(self.currently_logged_in_email).child("shopping_list").get()

    def update_favorites(self, data):
        self.db.child("users").child(self.currently_logged_in_email).child("favorites").update(data)

    def update_shopping_list(self, data):
        self.db.child("users").child(self.currently_logged_in_email).child("shopping_list").update(data)

    def remove_favorites(self, shop_name):
        self.db.child("users").child(self.currently_logged_in_email).child("favorites").child(shop_name).remove()

    def store_user_data(self):
        app = MDApp.get_running_app()
        data = {"email": app.root.get_screen("register").ids.user_email.text,
                "date_of_birth": app.dob,
                "username": app.root.get_screen("register").ids.username.text,
                "timestamp": str(datetime.datetime.now()),
                "shopping_list": "",
                "favorites": "",
                }
        try:
            email = app.root.get_screen("register").ids.user_email.text.split(".")[0]
            self.db.child("users").child(email).set(data)
        except Exception:
            app.open_error_dialog("Error while storing user data")


