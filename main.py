import googlemaps

from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.utils import platform
from kivy_garden.mapview import MapMarker
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from plyer import gps

from api_key import google_api_key
from components import DialogContent, ForgottenPwContent, ExpansionContent, PicDialogContent
from controller import Controller
from database import Database

# from android.permissions import request_permissions, Permission

# from webview import WebView

# from plyer import notification

# from pdfview import PdfView

if platform == "win":
    Window.size = 360, 640


class EasyShopping(MDApp):
    dialog = None
    dob = None
    gps = None
    item_list_dialog = None
    database = Database()
    controller = Controller()
    pdfview = None
    gps_status = StringProperty()
    lat = None
    lon = None
    api_key = google_api_key

    def build(self):
        self.icon = "img/icon.png"

        # Configure the gps
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            self.gps = True
        except NotImplementedError as e:
            self.gps = False
            self.lat = 46.254990
            self.lon = 18.978990
            print(e)

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file("kivy_lang/main.kv")

    def on_start(self):
        if platform == "android":
            from android_permissions import AndroidPermissions
            self.dont_gc = AndroidPermissions(self.start_app)

        # Add the Search Panel Widget to the Home Screen
        self.root.get_screen("nav").ids.search_container.add_widget(
            MDExpansionPanel(
                icon="magnify",
                content=ExpansionContent(),
                panel_cls=MDExpansionPanelOneLine(text="Keresés"),
            )
        )
        # Adding the markers of the nearby shops on the map
        # self.add_markers()

    def start_app(self):
        self.dont_gc = None

    def on_resume(self):
        if self.pdfview:
            self.pdfview.resume()

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
        self.lat = kwargs["lat"]
        self.lon = kwargs["lon"]

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    # This method is using the Places API from Google to search for given keywords e.g. "shops" in a
    # radius around the given coords and then returns a list of matching coordinates
    @staticmethod
    def search_places(api_key, lat, lon, radius, keyword):
        client = googlemaps.Client(api_key)

        search_params = {
            'location': f'{lat},{lon}',
            'radius': radius,
            'keyword': keyword
        }

        places = client.places_nearby(**search_params)

        coords = []
        for place in places['results']:
            lat = place['geometry']['location']['lat']
            lon = place['geometry']['location']['lng']
            coords.append((lat, lon))

        return coords

    # Adding the MapMarker widgets to the MapView with the right coordinates
    def add_markers(self):
        radius = 15000  # 1000 = 1 km
        keyword = "supermarket"
        shop_coords = self.search_places(self.api_key, self.lat, self.lon, radius, keyword)

        for coord in shop_coords:
            marker = MapMarker(lat=coord[0], lon=coord[1])
            print(coord)
            self.root.get_screen("nav").ids.mapview.add_widget(marker)

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

    def view_pdf(self, shop_name, b=None):
        """path = "shops/" + shop_name + ".pdf"
        storage_path = self.database.storage.child(path).get_url(None)
        # self.pdfview = PdfView(path)

        if platform == "android":
            self.pdfview = WebView(storage_path,
                                   enable_javascript=True,
                                   enable_downloads=True,
                                   enable_zoom=True, )"""

        pass

    def view_card_pic(self, pic_name):
        path = "images/" + self.database.currently_logged_in_email + "/" + pic_name + ".jpg"
        storage_path = self.database.storage.child(path).get_url(None)
        """self.pdfview = WebView(storage_path)"""
        print(storage_path)

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
            self.database.auth.send_password_reset_email(value)
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

    def open_error_dialog_with_register_btn(self, error_text):
        close_button = MDFillRoundFlatButton(text="Vissza", on_release=self.close_dialog)
        reg_button = MDFillRoundFlatButton(text="Regisztrálok", on_release=self.go_to_reg_after_dialog)
        self.dialog = MDDialog(title="Sikeres regisztráció", text=error_text,
                               size_hint=(1, None), buttons=[close_button, reg_button])
        self.dialog.open()

    def go_to_reg_after_dialog(self, obj):
        self.close_dialog(obj)
        self.controller.go_to_register_screen()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def close_dialog_go_to_home(self, obj):
        self.dialog.dismiss()
        self.controller.go_to_home_screen()

    def close_dialog_go_to_register(self, obj):
        self.dialog.dismiss()
        self.controller.go_to_home_screen()
        self.controller.go_to_register_screen()

    def check_if_registered(self):
        if self.database.check_if_registered():
            return
        else:
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
