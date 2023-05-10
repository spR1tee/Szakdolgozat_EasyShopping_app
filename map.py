import googlemaps
from kivy_garden.mapview import MapMarker
from kivymd.app import MDApp

from api_key import google_api_key


class Map:
    def __init__(self):
        self.api_key = google_api_key
        self.lat = None
        self.lon = None
        self.address_list = []

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
            # print(places["results"])
            print(place["vicinity"])  # Getting the address of the place
        return coords

    # Adding the MapMarker widgets to the MapView with the right coordinates
    def add_markers(self, radius, keyword):
        app = MDApp.get_running_app()
        # radius = 5000  # 1000 = 1 km
        # keyword = "cba"
        shop_coords = self.search_places(self.api_key, self.lat, self.lon, radius, keyword)

        for coord in shop_coords:
            marker = MapMarker(lat=coord[0], lon=coord[1])
            # print(coord)
            app.root.get_screen("nav").ids.mapview.add_widget(marker)