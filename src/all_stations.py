# import flet as ft
# import json
# import urllib

# class AllStations:
#     def __init__(self, server_value, tag_value):
#         self.server_value = server_value
#         self.tag_value = tag_value
#         print(f"Set tag value to: {tag_value}")

#     def get_all_stations(self):
#         if self.tag_value:
#             url = f"https://{self.server_value}/json/stations/bytag/{self.tag_value}"
#             print(url)
#             data = urllib.request.urlopen(url).read()
#             parsed_data = json.loads(data)
#             return parsed_data

    
import flet as ft
import json
import urllib

import asyncio
import aiohttp
import ijson
import time

class AllStations:
    def __init__(self, server_value, tag_value, coutrntry_codes):
        self.server_value = server_value
        self.tag_value = tag_value
        self.coutrntry_codes = coutrntry_codes
        print(f"Set tag value to: {tag_value}")

        
        

    async def get_all_stations(self):
        
        start_time = time.time()
        objects = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://{self.server_value}/json/stations/bytag/{self.tag_value}") as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch stations: {response.status}")
                    async for item in ijson.items_async(response.content, 'item'):
                        try:
                                objects.append(item)
                                if len(objects) % 1000 == 0:
                                    print(f"Fetched {len(objects)} stations so far...")
                        except Exception as e:
                            print(f"Error parsing item: {e}")
                    print(f"Fetched {len(objects)} stations in {time.time() - start_time:.2f} seconds")
                    # print(objects)
                    return objects
        except Exception as e:
            print(f"Error fetching stations: {e}")
            return []













    async def fetch_country_codes(self):
        start_time = time.time()
        country_codes = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://{self.server_value}/json/countries") as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch country codes: {response.status}")
                    async for item in ijson.items_async(response.content, 'item'):
                        try:
                                country_codes.append(item["name"])
                                if len(country_codes) % 100 == 0:
                                    print(f"Fetched {len(country_codes)} country codes so far...")
                        except Exception as e:
                            print(f"Error parsing item: {e}")
                    print(f"Fetched {len(country_codes)} country codes in {time.time() - start_time:.2f} seconds")
                    print(country_codes)
                    return country_codes
        except Exception as e:
            print(f"Error fetching country codes: {e}")
            return []