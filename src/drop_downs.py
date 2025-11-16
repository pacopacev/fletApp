import flet as ft
from datetime import datetime
from severs import Servers
from all_stations import AllStations
from snackbar import Snackbar
from global_model import GlobalModel
from validate_radio import ValidateRadio
import uuid

class DDComponents:
    def __init__(self, page, on_radio_change=None):
        self.server_value = None
        self.tag_value = None
        self.radio_value = None
        self.radios = None
        self.on_radio_change = on_radio_change
        self.page = page
        self.coutrntry_codes = None
        self.coutrntry_code = None
        self.now_playing_text = None
        self.now_playing = None
        self.now_playing_container = ft.Container()  
        self.border_color = ft.Colors.BLACK
     
        self.ddServer = ft.Dropdown(
            trailing_icon=ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.BLACK),
            leading_icon=ft.Icon(ft.Icons.PUBLIC, color=ft.Colors.BLACK),
            label="Server",
            label_style=ft.TextStyle(color=ft.Colors.BLACK),
            on_change=self.server_change,
            width=300,
            hint_text="Select Server",
            border_color=self.border_color,
            filled=True,
            options=[],
        )
        self.ddGenre = ft.Dropdown(
            trailing_icon=ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.BLACK),
            leading_icon=ft.Icon(ft.Icons.MUSIC_NOTE, color=ft.Colors.BLACK),
            label="Tag",
            label_style=ft.TextStyle(color=ft.Colors.BLACK),
            on_change=self.tag_change,
            width=300,
            hint_text="Select Genre",
            border_color=self.border_color,
            options=[
                ft.dropdown.Option("punk", "Punk"),
                ft.dropdown.Option("metal", "Metal"),
                ft.dropdown.Option("rock", "Rock"),
                ft.dropdown.Option("grindcore", "Grindcore"),
                ft.dropdown.Option("core", "Core"),
                ft.dropdown.Option("metalcore", "Metalcore"),
                ft.dropdown.Option("deathcore", "Deathcore"),
                ft.dropdown.Option("death_metal", "Death Metal"),
                ft.dropdown.Option("black_metal", "Black Metal"),
            ],
            filled=True,
            value=None,
        )
        
        self.ddCountry = ft.Dropdown(
            trailing_icon=ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.BLACK),
            leading_icon=ft.Icon(ft.Icons.FLAG, color=ft.Colors.BLACK),
            label="Country",
            label_style=ft.TextStyle(color=ft.Colors.BLACK),
            on_change=self.get_country_code,    
            width=300,
            hint_text="Select Country",
            border_color=self.border_color,
            options=[

            ],
            filled=True,
            disabled=True
        )
        
        self.ddRadio = ft.Dropdown(
            trailing_icon=ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.BLACK),
            leading_icon=ft.Icon(ft.Icons.RADIO, color=ft.Colors.BLACK),
            label="Radio Stations",
            label_style=ft.TextStyle(color=ft.Colors.BLACK),
            # on_click=self.on_radio_click,
            on_change=self.radio_change,
            width=300,
            border_color=self.border_color,
            hint_text="Select Radio",
            options=[],
            filled=True,
        )
        
        self.now_playing_text_container = None

        hosts = Servers().get_radiobrowser_base_urls()
        for host in hosts:
            # print(host)
            # print (host[:3].upper())
            self.ddServer.options.append(ft.dropdown.Option(key=host, text=host[:3].upper()))
    
    
    @staticmethod
    def toggle_border_color(page, self, e, dds):
        if page.theme_mode == "dark":
            page.theme_mode = "dark"
            for dd in dds:
                dd.border_color = ft.Colors.BLACK
                dd.border_width = 1
            page.theme_mode = "light"
        else: 
            page.theme_mode = "dark"
            for dd in dds:
                dd.border_color = ft.Colors.WHITE
                dd.border_width = 15
                dd.label_style.color = ft.Colors.BLACK
                dd.fill_color = ft.Colors.WHITE
                dd.border_radius = ft.border_radius.all(10)
        page.update()
        
    async def server_change(self, e):
        self.server_value = e.control.value
        print(f"Selected server: {self.server_value}")
        


        self.coutrntry_codes = await AllStations(self.server_value, self.tag_value, self.coutrntry_code).fetch_country_codes()
        await self.set_countruy_codes(self.coutrntry_codes)
        
        
        self.ddRadio.options.clear()

        if self.tag_value == None:
            print("No tag selected")
            snackbar_instance = Snackbar("Plase select a tag",bgcolor="red", length = None)
            snackbar_instance.open = True
            self.page.controls.append(snackbar_instance)
            self.page.update()
            return
        
              
        else:
            print("Loading radio stations...")
            try:  
                self.radios = await AllStations(self.server_value, self.tag_value, self.coutrntry_code).get_all_stations()

                # Add new radio options
                for radio in self.radios:
                    radio_name = f"{radio['name']} - {radio.get('bitrate', 'N/A')} Kbps"
                    self.ddRadio.options.append(
                        ft.dropdown.Option(
                            key=radio["url"], 
                            text=radio_name
                        )
                    )
                
                # Update the dropdown
                self.ddRadio.update()
                print(f"Loaded {len(self.radios)} radio stations")
                
            except Exception as ex:
                print(f"Error loading stations: {ex}")

    
    async def tag_change(self, e):
        
        print(f"Selected tag: {e.control.value}")
        self.tag_value = e.control.value
        if self.server_value == None:
            print("No server selected")
            snackbar_instance = Snackbar("No server selected", bgcolor="red", length = None)
            snackbar_instance.open = True
            self.page.controls.append(snackbar_instance)
            self.page.update()
            return    
        try:
                 
                self.ddRadio.options.clear()
                
                self.radios = await AllStations(self.server_value, self.tag_value, self.coutrntry_code).get_all_stations()
                
            
                for radio in self.radios:
                    radio_name = f"{radio['name']} - {radio.get('bitrate', 'N/A')} Kbps"
                    self.ddRadio.options.append(
                        ft.dropdown.Option(
                            key=radio["url"], 
                            text=radio_name,
                            data={
                                "favicon": radio.get("favicon", ""),
                                "stationuuid": radio.get("stationuuid", ""),
                                }
                        )
                    )
                
                # Update the dropdown
                self.ddRadio.update()
                print(f"Loaded {len(self.radios)} radio stations")
                length = len(self.radios)
                snackbar_instance = Snackbar("Loaded radio stations", bgcolor="green", length = length)
                snackbar_instance.open = True  
                self.page.controls.append(snackbar_instance)
                self.page.update()
                
        except Exception as ex:
            print(f"Error loading stations: {ex}")
    
    async def radio_change(self, e):
        
        if e.control.value:
            # print(self.ddRadio.options)
            radio_details = next((opt for opt in self.ddRadio.options if opt.key == self.ddRadio.value), None)
            favicon = str(next((opt.data.get("favicon") for opt in self.ddRadio.options if opt.key == self.ddRadio.value), None))
            stationuuid = str(next((opt.data.get("stationuuid") for opt in self.ddRadio.options if opt.key == self.ddRadio.value), None))
            
            if radio_details:
                radio_status = await ValidateRadio().validate_stream(radio_details.key)
                # print(f"Radio URL: {radio_details.key}, Valid: {radio_status}")
                if radio_status[0] == True:
                    self.radio_value = e.control.value
                    await self.on_radio_change(str(radio_details.key), str(radio_status[1]), radio_details.text, favicon) 
                    # print(f"Radio stream is valid: {radio_status[1]}")
                    snackbar_instance = Snackbar("💀 Radio stream is VALID! 🖤 Let the darkness play! 🌑", bgcolor="green", length = None)
                    snackbar_instance.open = True
                    self.page.controls.append(snackbar_instance)
                    self.page.update()
                    uuid = stationuuid if stationuuid != "" else ""
                    result_uuid_exist = await self.check_exist_station_uuid(uuid)
                    # print(result_uuid_exist)
                    if len(result_uuid_exist) == 0:
                        await self.insert_radio_to_db(radio_details.text, str(radio_status[1]), favicon, uuid)
                   
                else:
                    print(f"Radio stream is NOT valid: {radio_details.text}")
                    snackbar_instance = Snackbar("Radio stream is NOT valid", bgcolor="red", length = None)
                    snackbar_instance.open = True
                    self.page.controls.append(snackbar_instance)
                    self.page.update()

    async def on_radio_click(self, e):
        print("Radio dropdown focused")
        self.page.update()

    async def set_countruy_codes(self, country_codes):
        #print(self.coutrntry_codes)
        self.ddCountry.options.clear()
        for code in country_codes:
            self.ddCountry.options.append(ft.dropdown.Option(code))
        self.ddCountry.update()

    async def get_country_code(self, e):
        # print(e.control.value)
        self.coutrntry_code = e.control.value
        if self.coutrntry_code == None:
            print("No country selected")
            snackbar_instance = Snackbar("No country selected", bgcolor="red", length = None)
            snackbar_instance.open = True
            self.page.controls.append(snackbar_instance)
            self.page.update()
            return
        try:
                 # Clear existing radio options
                self.ddRadio.options.clear()
                # Get stations for the selected server
                self.radios = await AllStations(self.server_value, self.tag_value, self.coutrntry_code).get_all_stations()
                
                # Add new radio options
                for radio in self.radios:
                    radio_name = f"{radio['name']} - {radio.get('bitrate', 'N/A')} Kbps"
                    self.ddRadio.options.append(
                        ft.dropdown.Option(
                            key=radio["url"], 
                            text=radio_name
                        )
                    )
                
                # Update the dropdown
                self.ddRadio.update()
                print(f"Loaded {len(self.radios)} radio stations")
                length = len(self.radios)
                snackbar_instance = Snackbar("Loaded radio stations", bgcolor="green", length = length)
                snackbar_instance.open = True  
                self.page.controls.append(snackbar_instance)
                self.page.update()
                
        except Exception as ex:
            print(f"Error loading stations: {ex}")
            
    
    async def insert_radio_to_db(self, name, url, favicon, uuid):
        print("Inserting radio to database")
        favicon = favicon if favicon else "None"
        
        try:
            global_model = GlobalModel()
            await global_model.execute_query_all(
                "INSERT INTO flet_radios (name, url, favicon_url, uuid,created_at) VALUES (%s, %s, %s, %s, %s);",
                (name, url, favicon, uuid, datetime.now())
            )
            print("Radio inserted into database")           
        except Exception as ex:
            print(f"Error inserting radio into database: {ex}")
            
    # async def set_now_playing(self, text):

    #     self.now_playing_container.content = ft.Column(
    #         controls=[
    #             ft.Text(f"Now Playing: {text}", size=16, weight=ft.FontWeight.BOLD)
    #         ],  
    #         alignment=ft.MainAxisAlignment.CENTER,
    #     )
    #     self.now_playing_container.bgcolor = "#B00020"
    #     self.now_playing_container.padding = 20
    #     self.now_playing_container.border_radius = ft.border_radius.all(10)
    #     self.now_playing_container.width = 400
    #     self.now_playing_container.update()
    async def check_exist_station_uuid(self, stationuuid):
        # print(stationuuid)
        global_model = GlobalModel()
        result = await global_model.execute_query_all("SELECT * FROM flet_radios WHERE uuid = %s", (stationuuid,))
        return result
       
            
        
      



           
