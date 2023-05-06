from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


class LoginScreen(Screen):
    pass


class RegisterScreen(Screen):
    pass


class NavigationScreen(Screen):
    pass


class CameraScreen(Screen):
    preview = ObjectProperty(None)

    def __init__(self, **args):
        super().__init__(**args)

    def on_enter(self):
        app = MDApp.get_running_app()
        self.preview = app.root.get_screen("camera").ids.preview
        self.preview.connect_camera(filepath_callback=self.capture_path)

    def on_pre_leave(self):
        self.preview.disconnect_camera()

    def take_photo(self):
        self.preview.capture_photo()

    def capture_path(self, file_path):
        app = MDApp.get_running_app()
        app.database.upload_card_pic(file_path)

