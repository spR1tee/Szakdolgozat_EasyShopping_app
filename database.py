import datetime
import shutil
import time
from io import BytesIO

import fitz
import pyrebase
import requests
from kivymd.app import MDApp
from kivymd.toast import toast

from components import ShopCard, ListItemWithCheckbox, PicListItem

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
        self.card_name = None
        self.type = "all"

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
            self.upload_shops()
            app.controller.go_to_nav_screen()
            self.upload_shopping_list()
            self.load_cards()
            self.refresh_favorites()
        except Exception:
            app.open_error_dialog("Nem megfelelő felhasználónév vagy jelszó!")

    def join_as_guest(self):
        app = MDApp.get_running_app()
        login = self.auth.sign_in_anonymous()
        self.currently_logged_in_token = login["idToken"]
        self.currently_logged_in_token = self.auth.refresh(login["refreshToken"])
        self.upload_shops()
        app.controller.go_to_nav_screen()
        app.controller.go_to_home_screen()

    def log_out(self):
        app = MDApp.get_running_app()
        if self.auth.current_user is not None:
            self.auth.current_user = None
            self.currently_logged_in_email = None
        app.controller.go_to_login_screen()

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

    def get_cards(self):
        return self.db.child("users").child(self.currently_logged_in_email).child("cards").get()

    def update_cards(self, data):
        self.db.child("users").child(self.currently_logged_in_email).child("cards").update(data)

    def remove_cards(self, name):
        self.db.child("users").child(self.currently_logged_in_email).child("cards").child(name).remove()

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
                "cards": "",
                }
        try:
            email = app.root.get_screen("register").ids.user_email.text.split(".")[0]
            self.db.child("users").child(email).set(data)
        except Exception:
            app.open_error_dialog("Error while storing user data")

    # Takes the text from the input and then iterates through the stored pdfs in the Firebase Storage for matching
    # pattern and if found then displaying the shops, which contain the found item in their newspaper
    def perform_search(self, text):
        app = MDApp.get_running_app()
        pdfs = []
        found_text = []
        """all_shops = self.database.get_all_shops()
        for shop in all_shops.each():
            pdfs.append(shop.key() + ".pdf")"""

        pdfs = ["aldi.pdf", "spar.pdf"]

        for pdf in pdfs:
            path = "shops/" + pdf
            storage_path = self.storage.child(path).get_url(None)  # building storage path
            response = requests.get(storage_path)  # getting the content from the storage
            mem_area = BytesIO(response.content)  # getting the stream of the content
            doc = fitz.open(stream=mem_area, filetype="pdf")  # opening the stream and then searching in it
            for page in doc:
                if text.lower() in page.get_text().lower():
                    found_text.append(pdf.split(".")[0])
                    break

        favs = self.check_favorites()  # checking favorites, so we can display it with the right icon

        app.root.get_screen("nav").ids.shops_grid.clear_widgets()  # clearing all shop card widgets from the screen

        for found in found_text:
            self.create_card(found, favs)  # creating and adding the shop cards to the screen

    # Loading all shops and their cards on the main page after starting the app
    def upload_shops(self):
        all_shops = self.get_all_shops()
        favs = self.check_favorites()

        for shop in all_shops.each():
            self.create_card(shop.key(), favs)

    # Creating a shop card widget with the given name and content
    def create_card(self, shop_name, favorites):
        app = MDApp.get_running_app()
        img_path = "img/" + str(shop_name) + ".png"
        app.root.get_screen("nav").ids.shops_grid.add_widget(
            ShopCard(
                text=str(shop_name).title(),
                image=img_path,
                shop_name=str(shop_name),
                icon="heart" if shop_name in favorites else "heart-outline",
            )
        )

    # Adding item to the shopping list
    def add_item_to_shopping_list(self, item):
        app = MDApp.get_running_app()
        if item.text != "":
            app.root.get_screen("nav").ids.container.add_widget(ListItemWithCheckbox(text=item.text))
            data = {item.text: 0}
            self.update_shopping_list(data)
            item.text = ""
        else:
            app.open_error_dialog("Add meg a termék nevét!")

    # Adding item to the cards
    def add_item_to_cards(self, item):
        app = MDApp.get_running_app()
        if item.text != "":
            app.root.get_screen("nav").ids.card_container.add_widget(PicListItem(text=item.text))
            data = {item.text : ""}
            self.update_cards(data)
            self.card_name = item.text
            item.text = ""
            app.root.current = "camera"
        else:
            app.open_error_dialog("Add meg a termék nevét!")

    # Uploading the picture taken by the user to the Firebase Storage
    def upload_card_pic(self, path):
        app = MDApp.get_running_app()
        db_path = "images/" + self.currently_logged_in_email + "/" + self.card_name + ".jpg"
        self.storage.child(db_path).put(path)
        print(path)
        self.card_name = None
        shutil.rmtree(path.split("\\")[1])
        time.sleep(2)
        app.root.current = "nav"

    # Reloading the shopping list of the user from the database after starting the app
    def upload_shopping_list(self):
        app = MDApp.get_running_app()
        shopping_list = self.get_shopping_list()
        try:
            if shopping_list.each() is not None:
                for item in shopping_list.each():
                    if item.val() == 0:
                        add_item = ListItemWithCheckbox(text=item.key())
                        app.root.get_screen("nav").ids.container.add_widget(add_item)
                    elif item.val() == 1:
                        add_item = ListItemWithCheckbox(text="[s]" + item.key() + "[/s]")
                        add_item.ids.check.active = True
                        app.root.get_screen("nav").ids.container.add_widget(add_item)
        except Exception as e:
            print(e)

    # Method for load the users cards from database when starting the app

    def load_cards(self):
        app = MDApp.get_running_app()
        cards = self.get_cards()
        try:
            if cards.each() is not None:
                for item in cards.each():
                    add_item = PicListItem(text=item.key())
                    app.root.get_screen("nav").ids.card_container.add_widget(add_item)
        except Exception as e:
            print(e)

    # This method makes the filtering after any change made to the category selector (Swiper)
    def filter_shops(self, shop_type):
        app = MDApp.get_running_app()
        app.root.get_screen("nav").ids.shops_grid.clear_widgets()
        self.type = shop_type

        if shop_type == "all":
            self.upload_shops()
            return

        all_shops = self.get_all_shops()
        favs = self.check_favorites()

        for shop in all_shops.each():
            if shop.val()["type"] == shop_type:
                self.create_card(shop.key(), favs)

    # Adding or removing shops to/from the favorites, the function is not available for Guests
    def add_to_favorites(self, shop_name):
        if not self.check_if_registered():
            toast("Be kell jelentkezned ahhoz, hogy a kedvenceidhez add!")
            return

        favorites = self.get_favorites()

        if favorites.each() is not None:
            for fav in favorites.each():
                if fav.key() == shop_name:
                    self.remove_favorites(shop_name)
                    self.refresh_favorites()
                    return

        data = {shop_name: ""}
        self.update_favorites(data)
        self.refresh_favorites()

    # After adding or removing favorites this function is refreshing the displayed shop cards
    def refresh_favorites(self):
        app = MDApp.get_running_app()
        if not self.check_if_registered():
            toast("Regisztrálj, hogy láthasd a kedvenceidet!")
            return

        app.root.get_screen("nav").ids.favs_grid.clear_widgets()
        favorites = self.get_favorites()
        if favorites.each() is not None and favorites.each() != "":
            for fav in favorites.each():
                img_path = "img/" + str(fav.key()) + ".png"
                app.root.get_screen("nav").ids.favs_grid.add_widget(
                    ShopCard(
                        text=str(fav.key()).title(),
                        image=img_path,
                        shop_name=str(fav.key()),
                        icon="heart",
                    )
                )
        app.root.get_screen("nav").ids.shops_grid.clear_widgets()
        self.filter_shops(self.type)






