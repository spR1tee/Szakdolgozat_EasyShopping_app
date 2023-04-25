from io import BytesIO

import fitz
import googlemaps
import requests
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.utils import platform
from kivy_garden.mapview import MapMarker
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from plyer import gps

from api_key import google_api_key
from components import DialogContent, ListItemWithCheckbox, ShopCard, ForgottenPwContent, ExpansionContent
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
    item_list_dialog = None
    type = "all"
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
        except NotImplementedError as e:
            self.lat = 46.254990
            self.lon = 18.978990
            print(e)

        # Request permission for using location on Android
        if platform == "android":
            self.request_location_permission()

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file("kivy_lang/main.kv")

    def on_start(self):
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

    def close_dialog_new(self):
        self.item_list_dialog.dismiss()

    def request_location_permission(self):
        """request_permissions([Permission.ACCESS_COARSE_LOCATION,
                            Permission.ACCESS_FINE_LOCATION])"""
        pass

    # Takes the text from the input and then iterates through the stored pdfs in the Firebase Storage for matching
    # pattern and if found then displaying the shops, which contain the found item in their newspaper
    def perform_search(self, text):
        pdfs = []
        found_text = []
        """all_shops = self.database.get_all_shops()
        for shop in all_shops.each():
            pdfs.append(shop.key() + ".pdf")"""

        pdfs = ["aldi.pdf", "spar.pdf"]

        for pdf in pdfs:
            path = "shops/" + pdf
            storage_path = self.database.storage.child(path).get_url(None)  # building storage path
            response = requests.get(storage_path)  # getting the content from the storage
            mem_area = BytesIO(response.content)  # getting the stream of the content
            doc = fitz.open(stream=mem_area, filetype="pdf")  # opening the stream and then searching in it
            for page in doc:
                if text in page.get_text():
                    found_text.append(pdf.split(".")[0])
                    break

        favs = self.database.check_favorites()  # checking favorites, so we can display it with the right icon

        self.root.get_screen("nav").ids.shops_grid.clear_widgets()  # clearing all shop card widgets from the screen

        for found in found_text:
            self.create_card(found, favs)  # creating and adding the shop cards to the screen

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

    # Adding item to the shopping list
    def add_item(self, item):
        if item.text != "":
            self.root.get_screen("nav").ids.container.add_widget(ListItemWithCheckbox(text=item.text))
            print(item.text)
            data = {item.text: 0}
            self.database.update_shopping_list(data)
            item.text = ""
        else:
            self.open_error_dialog("Add meg a termék nevét!")

    # Creating a shop card widget with the given name and content
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

    # Reloading the shopping list of the user from the database after starting the app
    def upload_shopping_list(self):
        shopping_list = self.database.get_shopping_list()
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

    # This method makes the filtering after any change made to the category selector (Swiper)
    def filter_shops(self, shop_type):
        print(shop_type)
        self.root.get_screen("nav").ids.shops_grid.clear_widgets()
        self.type = shop_type

        if shop_type == "all":
            self.upload_shops()
            return

        all_shops = self.database.get_all_shops()
        favs = self.database.check_favorites()

        for shop in all_shops.each():
            if shop.val()["type"] == shop_type:
                self.create_card(shop.key(), favs)

    # Adding or removing shops to/from the favorites, the function is not available for Guests
    def add_to_favorites(self, shop_name):
        if not self.database.check_if_registered():
            toast("Be kell jelentkezned ahhoz, hogy a kedvenceidhez add!")
            return

        favorites = self.database.get_favorites()

        if favorites.each() is not None:
            for fav in favorites.each():
                if fav.key() == shop_name:
                    self.database.remove_favorites(shop_name)
                    self.refresh_favorites()
                    return

        data = {shop_name: ""}
        self.database.update_favorites(data)
        self.refresh_favorites()

    # Loading all shops and their cards on the main page after starting the app
    def upload_shops(self):
        all_shops = self.database.get_all_shops()
        favs = self.database.check_favorites()

        for shop in all_shops.each():
            self.create_card(shop.key(), favs)

    # After adding or removing favorites this function is refreshing the displayed shop cards
    def refresh_favorites(self):
        if not self.database.check_if_registered():
            toast("Regisztrálj, hogy láthasd a kedvenceidet!")
            return

        self.root.get_screen("nav").ids.favs_grid.clear_widgets()
        favorites = self.database.get_favorites()
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
