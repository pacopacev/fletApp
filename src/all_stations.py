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
    def __init__(self, server_value, tag_value):
        self.server_value = server_value
        self.tag_value = tag_value
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
                            if self.tag_value:
                                if 'tags' in item and self.tag_value in item['tags']:
                                    objects.append(item)
                            else:
                                objects.append(item)
                                if len(objects) % 1000 == 0:
                                    print(f"Fetched {len(objects)} stations so far...")
                        except Exception as e:
                            print(f"Error parsing item: {e}")
                    print(f"Fetched {len(objects)} stations in {time.time() - start_time:.2f} seconds")
                    return objects
        except Exception as e:
            print(f"Error fetching stations: {e}")
            return []