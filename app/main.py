from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from plyer import gps

from components import ExpansionContent
from controller import Controller
from database import Database
from map import Map


# if platform == "win":
#    Window.size = 360, 640


class EasyShopping(MDApp):
    gps = None
    permission = None
    database = Database()
    googlemaps = Map()
    controller = Controller()
    gps_status = StringProperty()

    def build(self):
        # Configure the gps
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
        except NotImplementedError as e:
            self.googlemaps.lat = 46.25318
            self.googlemaps.lon = 18.97883
            print(e)

        self.icon = "assets/img/icon.png"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file("../kivy_lang/main.kv")

    def on_start(self):

        if platform == "android":
            from android_permissions import AndroidPermissions
            self.permission = AndroidPermissions(self.start_app)

        # Add the Search Panel Widget to the Home Screen
        self.root.get_screen("nav").ids.search_container.add_widget(
            MDExpansionPanel(
                icon="magnify",
                content=ExpansionContent(),
                panel_cls=MDExpansionPanelOneLine(text="Keresés"),
            )
        )

    def start_app(self):
        self.permission = None

    def on_resume(self):
        if self.controller.view:
            self.controller.view.resume()

        gps.start(1000, 0)

    def on_pause(self):
        gps.stop()
        return True

    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.googlemaps.lat = kwargs["lat"]
        self.googlemaps.lon = kwargs["lon"]

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)


if __name__ == '__main__':
    EasyShopping().run()
