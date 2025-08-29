import flet as ft
import json
import urllib

class AllStations:
    def __init__(self, server_value, tag_value):
        self.server_value = server_value
        self.tag_value = tag_value
        print(f"Set tag value to: {tag_value}")

    def get_all_stations(self):
        if self.tag_value:
            url = f"https://{self.server_value}/json/stations/bytag/{self.tag_value}"
            print(url)
            data = urllib.request.urlopen(url).read()
            parsed_data = json.loads(data)
            return parsed_data

    
