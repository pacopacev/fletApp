import flet as ft
from datetime import datetime
from severs import Servers
from all_stations import AllStations
from snackbar import Snackbar
from global_model import GlobalModel
from validate_radio import ValidateRadio

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
        

        self.ddServer = ft.Dropdown(
            on_change=self.server_change,
            width=300,
            hint_text="Select Server",
            border_color=ft.Colors.RED,
            options=[],
            
        )
        

        self.ddGenre = ft.Dropdown(
            on_change=self.tag_change,
            width=300,
            hint_text="Select Genre",
            border_color=ft.Colors.RED,
            options=[
                ft.dropdown.Option("metal", "Metal"),
                ft.dropdown.Option("rock", "Rock"),
                ft.dropdown.Option("grindcore", "Grindcore"),
                ft.dropdown.Option("core", "Core"),
                ft.dropdown.Option("metalcore", "Metalcore"),
                ft.dropdown.Option("deathcore", "Deathcore"),
                ft.dropdown.Option("death_metal", "Death Metal"),
                ft.dropdown.Option("black_metal", "Black Metal"),
            ],
            value=None,
        )
        
        self.ddCountry = ft.Dropdown(
            on_change=self.get_country_code,
            width=300,
            hint_text="Select Country",
            border_color=ft.Colors.RED,
            options=[

            ],
        )
        
        self.ddRadio = ft.Dropdown(
            # on_click=self.on_radio_click,
            on_change=self.radio_change,
            width=300,
            border_color=ft.Colors.RED,
            hint_text="Select Radio",
            options=[],
        )
        
        self.now_playing_text_container = None

        hosts = Servers().get_radiobrowser_base_urls()
        for host in hosts:
            # print(host)
            # print (host[:3].upper())
            self.ddServer.options.append(ft.dropdown.Option(key=host, text=host[:3].upper()))

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
                            text=radio_name,
                            data={
                                "favicon": radio.get("favicon", ""),
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
            favicon = next((opt.data.get("favicon") for opt in self.ddRadio.options if opt.key == self.ddRadio.value), None)
            
            if radio_details:
                radio_status = await ValidateRadio().validate_stream(radio_details.key)
                # print(f"Radio URL: {radio_details.key}, Valid: {radio_status}")
                if radio_status[0] == True:
                    self.radio_value = e.control.value
                    self.on_radio_change(self.radio_value, radio_status[1], radio_details.text, favicon) 
                    # print(f"Radio stream is valid: {radio_status[1]}")
                    snackbar_instance = Snackbar("💀 Radio stream is VALID! 🖤 Let the darkness play! 🌑", bgcolor="green", length = None)
                    snackbar_instance.open = True
                    self.page.controls.append(snackbar_instance)
                    self.page.update()
                    await self.insert_radio_to_db(radio_details.text, radio_status[1])
                    # await self.set_now_playing(radio_details.text)
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
            
    
    async def insert_radio_to_db(self, name, url):
        print("Inserting radio to database")
        try:
            global_model = GlobalModel()
            await global_model.execute_query_all(
                "INSERT INTO flet_radios (name, url, created_at) VALUES (%s, %s, %s);",
                (name, url, datetime.now())
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
         
            
        
      



           
