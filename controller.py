from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker

from components import DialogContent, PicDialogContent, ForgottenPwContent


# from webview import WebView

class Controller:
    def __init__(self):
        self.view = None
        self.dob = None
        self.dialog = None
        self.item_list_dialog = None

    def view_pdf(self, shop_name):
        """app = MDApp.get_running_app()
        path = "shops/" + shop_name + ".pdf"
        storage_path = app.database.get_storage_url(path)
        self.view = WebView(storage_path, enable_zoom=True)"""
        pass

    def view_card_pic(self, pic_name, b=None):
        app = MDApp.get_running_app()
        path = "images/" + app.database.userId + "/" + pic_name + ".jpg"
        storage_path = app.database.get_storage_url(path)
        """self.view = WebView(storage_path, enable_zoom=True)"""
        print(storage_path)

    # Dialog method for adding new item to the shopping list
    def show_item_dialog(self):
        if not self.item_list_dialog:
            self.item_list_dialog = MDDialog(
                title="Elem hozzáadása",
                type="custom",
                content_cls=DialogContent(),
            )

        self.item_list_dialog.open()

    # Dialog method for adding new item to the cards list
    def show_pic_dialog(self):
        if not self.item_list_dialog:
            self.item_list_dialog = MDDialog(
                title="Adj meg egy nevet az új kártyának!",
                type="custom",
                content_cls=PicDialogContent(),
            )

        self.item_list_dialog.open()

    def close_dialog_new(self):
        self.item_list_dialog.dismiss()

    def forgotten_password(self):
        content_cls = ForgottenPwContent()
        close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog)
        send_button = MDFillRoundFlatButton(text="E-mail küldése", on_release=lambda x: self.get_data(x, content_cls))
        self.dialog = MDDialog(title="Elfelejtett jelszó", size_hint=(1, None),
                               type="custom", buttons=[close_button, send_button],
                               content_cls=content_cls)
        self.dialog.open()

    def get_data(self, x, content_cls):
        app = MDApp.get_running_app()
        textfield = content_cls.ids.forgotten_pw_email
        value = textfield._get_text()
        if value != "":
            self.dialog.dismiss()
            app.database.auth.send_password_reset_email(value)
            print("success")
        else:
            self.open_error_dialog("Add meg az e-mail címed!")

        # hibakezelés TODO

    def open_error_dialog(self, error_text):
        close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Hiba", text=error_text,
                               size_hint=(1, None), buttons=[close_button])
        self.dialog.open()

    def open_success_dialog(self, success_text):
        close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Sikeres regisztráció", text=success_text,
                               size_hint=(1, None), buttons=[close_button])
        self.dialog.open()

    def open_error_dialog_with_register_btn(self, error_text):
        close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog)
        reg_button = MDFillRoundFlatButton(text="Regisztrálok", on_release=self.go_to_reg_after_dialog)
        self.dialog = MDDialog(title="Sikeres regisztráció", text=error_text,
                               size_hint=(1, None), buttons=[close_button, reg_button])
        self.dialog.open()

    def go_to_reg_after_dialog(self, obj):
        self.close_dialog(obj)
        self.go_to_register_screen()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def close_dialog_go_to_home(self, obj):
        self.dialog.dismiss()
        self.go_to_home_screen()

    def close_dialog_go_to_register(self, obj):
        self.dialog.dismiss()
        self.go_to_home_screen()
        self.go_to_register_screen()

    def check_if_registered(self):
        app = MDApp.get_running_app()
        if app.database.check_if_registered():
            return
        else:
            close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog_go_to_home)
            register_button = MDFillRoundFlatButton(text="Regisztrálok", on_release=self.close_dialog_go_to_register)
            self.dialog = MDDialog(title="Hiba",
                                   text="Sajnáljuk, de ez a funkció csak regisztrált felhasználók számára érhető el.",
                                   size_hint=(0.7, 1), buttons=[close_button, register_button])
            self.dialog.open()

    def on_save_date_picker(self, instance, value, date_range):
        app = MDApp.get_running_app()
        label = MDLabel(text=str(value), halign="center", adaptive_height=True, font_name="assets/fonts/Comfortaa-Regular.ttf",
                        adaptive_width=True)
        if self.dob is not None:
            app.root.get_screen("register").ids.dob_box.clear_widgets()
        self.dob = str(value)
        app.root.get_screen("register").ids.dob_box.add_widget(label)
        print(self.dob)

    def show_date_picker(self):
        date_dialog = MDDatePicker(title="VÁLASSZ DÁTUMOT", min_year=1910, max_year=2011, year=2000, month=1, day=1)
        date_dialog.bind(on_save=self.on_save_date_picker)
        date_dialog.open()

    @staticmethod
    def go_to_login_screen():
        app = MDApp.get_running_app()
        app.root.current = "login"

    @staticmethod
    def go_to_register_screen():
        app = MDApp.get_running_app()
        app.root.current = "register"

    @staticmethod
    def go_to_nav_screen():
        app = MDApp.get_running_app()
        app.root.current = "nav"

    @staticmethod
    def go_to_home_screen():
        app = MDApp.get_running_app()
        app.root.get_screen("nav").ids.bottom_nav.switch_tab("home")

    @staticmethod
    def go_to_shopping_list_screen():
        app = MDApp.get_running_app()
        app.root.get_screen("nav").ids.bottom_nav.switch_tab("shopping_list")

    @staticmethod
    def go_to_profile_screen():
        app = MDApp.get_running_app()
        app.root.get_screen("nav").ids.bottom_nav.switch_tab("profile")

    @staticmethod
    def go_to_camera_screen():
        app = MDApp.get_running_app()
        app.root.current = "camera"
