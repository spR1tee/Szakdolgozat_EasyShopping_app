import googlemaps
from kivy_garden.mapview import MapMarker
from kivymd.app import MDApp

from api_key import google_api_key


class GoogleMaps:
    def __init__(self):
        self.api_key = google_api_key
        self.lat = None
        self.lon = None

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
        app = MDApp.get_running_app()
        radius = 15000  # 1000 = 1 km
        keyword = "supermarket"
        shop_coords = self.search_places(self.api_key, app.lat, app.lon, radius, keyword)

        for coord in shop_coords:
            marker = MapMarker(lat=coord[0], lon=coord[1])
            print(coord)
            app.root.get_screen("nav").ids.mapview.add_widget(marker)