import flet as ft
from datetime import datetime
from severs import Servers
from all_stations import AllStations
from snackbar import Snackbar
from global_model import GlobalModel

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

        self.ddServer = ft.Dropdown(
            on_change=self.server_change,
            width=300,
            hint_text="Select Server",
            border_color=ft.Colors.RED,
            options=[],
            # helper_text="Select a server from the list",
            # helper_style=ft.TextStyle(color=ft.Colors.RED),         
            #value=None,
            
        )
        
        
        # self.ddServer.options.append(ft.dropdown.Option(key = "None", text="Select Server"))

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

        # Initialize server options


        hosts = Servers().get_radiobrowser_base_urls()
        server_name = ""
        for host in hosts:
            # print(host)
            # print (host[:3].upper())
            self.ddServer.options.append(ft.dropdown.Option(key=host, text=host[:3].upper()))

    async def server_change(self, e):
        self.server_value = e.control.value
        print(f"Selected server: {self.server_value}")
        


        self.coutrntry_codes = await AllStations(self.server_value, self.tag_value, self.coutrntry_code).fetch_country_codes()
        await self.set_countruy_codes(self.coutrntry_codes)
        
        
        # Clear existing radio optionss
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
        # AllStations(self.server_value, self.tag_value).get_all_stations()

    async def radio_change(self, e):
        self.radio_value = e.control.value
        if self.on_radio_change:
            self.on_radio_change(self.radio_value)
            radio_details = next((opt for opt in self.ddRadio.options if opt.key == self.ddRadio.value), None)
            if radio_details:
                # print(f"Radio selected: {radio_details.text} - {radio_details.key}")
                await self.insert_radio_to_db(radio_details.text, radio_details.key)

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
      



           
