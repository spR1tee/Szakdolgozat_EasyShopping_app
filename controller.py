from kivymd.app import MDApp


class Controller:
    def __init__(self):
        self.app = MDApp.get_running_app()

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
