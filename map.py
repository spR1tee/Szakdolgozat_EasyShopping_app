import googlemaps
from kivy_garden.mapview import MapMarker
from kivymd.app import MDApp

from api_key import google_api_key
from components import ThreeLineItem


class Map:
    def __init__(self):
        self.api_key = google_api_key
        self.lat = None
        self.lon = None
        self.address_list = []

    def focus_on_shop(self, x, lat, lon):
        app = MDApp.get_running_app()
        app.root.get_screen("nav").ids.mapview.center_on(lat, lon)
        app.root.get_screen("nav").ids.mapview.zoom = 18
        print(lat, lon)

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
            if place["name"].lower() == keyword.lower() or keyword.lower() in place["name"].lower():
                lat = place['geometry']['location']['lat']
                lon = place['geometry']['location']['lng']
                address = place['vicinity']
                name = place['name']
                if "opening_hours" in place.keys():
                    open_now = "Nyitva" if place['opening_hours']['open_now'] else "Zárva"
                else:
                    open_now = "Nincs adat"
                coords.append((lat, lon, name, address, open_now))
        return coords

    # Adding the MapMarker widgets to the MapView with the right coordinates
    def add_markers(self, radius, keyword):
        app = MDApp.get_running_app()

        if keyword == "" or radius == "":
            app.controller.open_error_dialog("Mindkét mezőt kötelező kitölteni!")
            return

        if not radius.isnumeric():
            app.controller.open_error_dialog("A körzetet kötelező számként megadni!")
            return

        if int(radius) > 150:
            app.controller.open_error_dialog("Túl nagy körzet!")
            return

        shop_coords = self.search_places(self.api_key, self.lat, self.lon, int(radius) * 1000, keyword)

        app.root.get_screen("nav").ids.places_container.clear_widgets()

        for coord in shop_coords:
            marker = MapMarker(lat=coord[0], lon=coord[1])
            app.root.get_screen("nav").ids.mapview.add_widget(marker)
            three_line_list_item = ThreeLineItem(
                text=coord[2],
                secondary_text=coord[3],
                tertiary_text=coord[4],
                lat=str(coord[0]),
                lon=str(coord[1])
            )
            print(three_line_list_item.lat)
            print(three_line_list_item.lon)
            three_line_list_item.bind(on_release=lambda x: self.focus_on_shop(x, float(three_line_list_item.lat),
                                                                              float(three_line_list_item.lon)))

            app.root.get_screen("nav").ids.places_container.add_widget(three_line_list_item)
