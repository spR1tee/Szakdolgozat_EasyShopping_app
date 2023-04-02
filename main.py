from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.card import MDCard
from plyer import notification
from kivy.core.window import Window
from controller import Controller
import datetime
# from webview import WebView
from plyer import gps
from plyer.utils import platform
import screens

Window.size = 360, 640


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


class ForgottenPwContent(MDBoxLayout):
    pass


class ShopCard(MDCard):
    text = StringProperty()
    image = StringProperty()
    id = StringProperty()
    pass


class EasyShopping(MDApp):
    dialog = None
    currently_logged_in_token = None
    data = None
    dob = None
    browser = None
    controller = Controller()

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file("kivy_lang/main.kv")

    def on_start(self):
        self.upload_shops()
        """if auth.current_user is None:
            self.go_to_login_screen()
        else:
            self.go_to_home_screen()"""

    # def view_google(self, b):
    #    self.browser = WebView('https://www.google.com',
    #                          enable_javascript=True,
    #                           enable_downloads=True,
    #                           enable_zoom=True)

    def notification_test(self, mode="normal"):
        notification.notify("Title", "Test notification message", "EasyShopping")

    def add_to_favorites(self):
        pass

    def upload_shops(self):
        all_shops = self.controller.db.child("shops").get()

        for shop in all_shops.each():
            img_path = "img/" + str(shop.key()) + ".png"
            self.root.get_screen("nav").ids.shops_grid.add_widget(
                ShopCard(
                    text=str(shop.key()).title(),
                    image=img_path,
                    id=str(shop.key()),
                )
            )

        """
        user email kiszedése realtime databaseből
        
        all_users = self.db.child("users").get()
        for user in all_users.each():
            print(user.key())
            print(user.val())
            print(user.val()["email"])
        """

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
        if value is not "":
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
                     "timestamp": str(datetime.datetime.now())
                     }
        try:
            self.controller.db.child("users").child(self.root.get_screen("register").ids.username.text).set(self.data)
        except Exception:
            self.open_error_dialog("Error while storing user data")

    def go_to_login_screen(self):
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
                               text="Sajnáljuk, de ez az oldal csak regisztrált felhasználók számára érhető el.",
                               size_hint=(0.7, 1), buttons=[close_button, register_button])
        self.dialog.open()

    def on_save_date_picker(self, instance, value, date_range):
        label = MDLabel(text=str(value), halign="center", adaptive_height=True, font_name="fonts/Comfortaa-Regular.ttf")
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
