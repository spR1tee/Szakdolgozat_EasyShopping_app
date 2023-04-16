import datetime
import os

import fitz
from urllib.request import Request, urlopen
from io import BytesIO

import requests
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker

from components import DialogContent, ListItemWithCheckbox, ShopCard, ForgottenPwContent, ExpansionContent
from controller import Controller

# from plyer import notification

# from pdfview import PdfView

Window.size = 360, 640


class WindowManager(ScreenManager):
    pass


class EasyShopping(MDApp):
    dialog = None
    data = None
    dob = None
    browser = None
    item_list_dialog = None
    type = "all"
    controller = Controller()
    pdfview = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file("kivy_lang/main.kv")

    def on_start(self):
        self.root.get_screen("nav").ids.search_container.add_widget(
            MDExpansionPanel(
                icon="magnify",
                content=ExpansionContent(),
                panel_cls=MDExpansionPanelOneLine(text="Keresés"),
            )
        )

    def on_resume(self):
        if self.pdfview:
            self.pdfview.resume()

    def show_item_dialog(self):
        if not self.item_list_dialog:
            self.item_list_dialog = MDDialog(
                title="Elem hozzáadása",
                type="custom",
                content_cls=DialogContent(),
            )

        self.item_list_dialog.open()

    def close_dialog_new(self):
        self.item_list_dialog.dismiss()

    def perform_search(self, text):
        pdfs = ["aldi.pdf", "spar.pdf"]
        found_text = []

        for pdf in pdfs:
            path = "shops/" + pdf
            # self.controller.storage.child(path).download(path, "downloaded.pdf")
            storage_path = self.controller.storage.child(path).get_url(None)
            r = requests.get(storage_path)
            f = BytesIO(r.content)
            # remoteFile = urlopen(Request(storage_path)).read()
            # memoryFile = StringIO(remoteFile)
            doc = fitz.open(stream=f, filetype="pdf")
            for page in doc:
                if text in page.get_text():
                    found_text.append(pdf.split(".")[0])
                    break

        """for pdf in pdfs:
            doc = fitz.open(pdf)
            for page in doc:
                if text in page.get_text():
                    found_text.append(pdf.split(".")[0])
                    break"""
        favs = self.check_favorites()

        self.root.get_screen("nav").ids.shops_grid.clear_widgets()
        for found in found_text:
            self.create_card(found, favs)

    def view_pdf(self, shop_name, b):
        # self.pdfview = PdfView(path)
        pass

    def add_item(self, item):
        if item.text != "":
            self.root.get_screen("nav").ids.container.add_widget(ListItemWithCheckbox(text=item.text))
            print(item.text)
            data = {item.text: 0}
            self.controller.db.child("users").child(self.controller.currently_logged_in_email).child(
                "shopping_list").update(data)
            item.text = ""
        else:
            self.open_error_dialog("Add meg a termék nevét!")

    def check_favorites(self):
        all_shops = self.controller.db.child("shops").get()
        in_fav = []
        if self.controller.auth.current_user is not None:
            if "registered" in self.controller.auth.current_user.keys():
                if self.controller.auth.current_user["registered"] is True:
                    favorites = self.controller.db.child("users").child(
                        self.controller.currently_logged_in_email).child(
                        "favorites").get()
                    if favorites.each() is not None and favorites.each() != "":
                        for shop in all_shops.each():
                            for fav in favorites.each():
                                if shop.key() == fav.key():
                                    in_fav.append(shop.key())

        return in_fav

    def create_card(self, shop_name, favorites):
        img_path = "img/" + str(shop_name) + ".png"
        self.root.get_screen("nav").ids.shops_grid.add_widget(
            ShopCard(
                text=str(shop_name).title(),
                image=img_path,
                shop_name=str(shop_name),
                icon="heart" if shop_name in favorites else "heart-outline",
            )
        )

    def upload_shopping_list(self):
        shopping_list = self.controller.db.child("users").child(self.controller.currently_logged_in_email).child(
            "shopping_list").get()
        try:
            if shopping_list is not None:
                for item in shopping_list.each():
                    if item.val() == 0:
                        add_item = ListItemWithCheckbox(text=item.key())
                        self.root.get_screen("nav").ids.container.add_widget(add_item)
                    elif item.val() == 1:
                        add_item = ListItemWithCheckbox(text="[s]" + item.key() + "[/s]")
                        add_item.ids.check.active = True
                        self.root.get_screen("nav").ids.container.add_widget(add_item)
                    print(item.key())
                    print(item.val())
        except Exception as e:
            print(e)
            pass

    def filter_shops(self, shop_type):
        print(shop_type)
        print(self.root.get_screen("nav").ids.tabs.get_current_tab().type)
        self.root.get_screen("nav").ids.shops_grid.clear_widgets()
        self.type = shop_type

        if shop_type == "all":
            self.upload_shops()
            return

        all_shops = self.controller.db.child("shops").get()
        favs = self.check_favorites()

        for shop in all_shops.each():
            if shop.val()["type"] == shop_type:
                self.create_card(shop.key(), favs)

    def add_to_favorites(self, shop_name):
        if "registered" not in self.controller.auth.current_user.keys():
            toast("Be kell jelentkezned ahhoz, hogy a kedvenceidhez add!")
            return

        favorites = self.controller.db.child("users").child(self.controller.currently_logged_in_email).child(
            "favorites").get()

        if favorites.each() is not None:
            for fav in favorites.each():
                if fav.key() == shop_name:
                    self.controller.db.child("users").child(self.controller.currently_logged_in_email).child(
                        "favorites").child(shop_name).remove()
                    self.refresh_favorites()
                    return

        data = {shop_name: ""}
        self.controller.db.child("users").child(self.controller.currently_logged_in_email).child(
            "favorites").update(data)
        self.refresh_favorites()

    def upload_shops(self):
        all_shops = self.controller.db.child("shops").get()
        favs = self.check_favorites()

        for shop in all_shops.each():
            self.create_card(shop.key(), favs)

    def refresh_favorites(self):
        if "registered" not in self.controller.auth.current_user.keys():
            self.root.get_screen("nav").ids.favs_grid.clear_widgets()
            self.root.get_screen("nav").ids.favs_grid.add_widget(
                MDLabel(
                    text="Regisztrálj"
                )
            )

        self.root.get_screen("nav").ids.favs_grid.clear_widgets()
        favorites = self.controller.db.child("users").child(self.controller.currently_logged_in_email).child(
            "favorites").get()
        if favorites.each() is not None and favorites.each() != "":
            for fav in favorites.each():
                img_path = "img/" + str(fav.key()) + ".png"
                self.root.get_screen("nav").ids.favs_grid.add_widget(
                    ShopCard(
                        text=str(fav.key()).title(),
                        image=img_path,
                        shop_name=str(fav.key()),
                        icon="heart",
                    )
                )
        self.root.get_screen("nav").ids.shops_grid.clear_widgets()
        self.filter_shops(self.type)

    def forgotten_password(self):
        content_cls = ForgottenPwContent()
        close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog)
        send_button = MDFillRoundFlatButton(text="E-mail küldése", on_release=lambda x: self.get_data(x, content_cls))
        self.dialog = MDDialog(title="Elfelejtett jelszó", size_hint=(1, None),
                               type="custom", buttons=[close_button, send_button],
                               content_cls=content_cls)
        self.dialog.open()

    def get_data(self, x, content_cls):
        textfield = content_cls.ids.forgotten_pw_email
        value = textfield._get_text()
        if value != "":
            self.dialog.dismiss()
            self.controller.auth.send_password_reset_email(value)
            print("success")
        else:
            self.open_error_dialog("Add meg az e-mail címed!")

        # hibakezelés TODO

    def open_error_dialog(self, error_text):
        close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Hiba", text=error_text,
                               size_hint=(1, None), buttons=[close_button])
        self.dialog.open()

    def open_success_dialog(self, error_text):
        close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Sikeres regisztráció", text=error_text,
                               size_hint=(1, None), buttons=[close_button])
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def close_dialog_go_to_home(self, obj):
        self.dialog.dismiss()
        self.go_to_home_screen()

    def close_dialog_go_to_register(self, obj):
        self.dialog.dismiss()
        self.go_to_home_screen()
        self.go_to_register_screen()

    def store_user_data(self):
        self.data = {"email": self.root.get_screen("register").ids.user_email.text,
                     "date_of_birth": self.dob,
                     "username": self.root.get_screen("register").ids.username.text,
                     "timestamp": str(datetime.datetime.now()),
                     "shopping_list": "",
                     "favorites": "",
                     }
        try:
            email = self.root.get_screen("register").ids.user_email.text.split(".")[0]
            self.controller.db.child("users").child(email).set(self.data)
        except Exception:
            self.open_error_dialog("Error while storing user data")

    def go_to_login_screen(self, x=None):
        self.root.current = "login"

    def go_to_register_screen(self):
        self.root.current = "register"

    def go_to_nav_screen(self):
        self.root.current = "nav"

    def go_to_home_screen(self):
        self.root.get_screen("nav").ids.bottom_nav.switch_tab("home")

    def go_to_shopping_list_screen(self):
        self.root.get_screen("nav").ids.bottom_nav.switch_tab("shopping_list")

    def go_to_profile_screen(self):
        self.root.get_screen("nav").ids.bottom_nav.switch_tab("profile")

    def check_if_registered(self):
        if "registered" in self.controller.auth.current_user.keys():
            if self.controller.auth.current_user["registered"] is True:
                return

        close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog_go_to_home)
        register_button = MDFillRoundFlatButton(text="Regisztrálok", on_release=self.close_dialog_go_to_register)
        self.dialog = MDDialog(title="Hiba",
                               text="Sajnáljuk, de ez a funkció csak regisztrált felhasználók számára érhető el.",
                               size_hint=(0.7, 1), buttons=[close_button, register_button])
        self.dialog.open()

    def on_save_date_picker(self, instance, value, date_range):
        label = MDLabel(text=str(value), halign="center", adaptive_height=True, font_name="fonts/Comfortaa-Regular.ttf",
                        adaptive_width=True)
        if self.dob is not None:
            self.root.get_screen("register").ids.dob_box.clear_widgets()
        self.dob = str(value)
        self.root.get_screen("register").ids.dob_box.add_widget(label)
        print(self.dob)

    def show_date_picker(self):
        date_dialog = MDDatePicker(title="VÁLASSZ DÁTUMOT", min_year=1910, max_year=2011, year=2000, month=1, day=1)
        date_dialog.bind(on_save=self.on_save_date_picker)
        date_dialog.open()


if __name__ == '__main__':
    EasyShopping().run()
