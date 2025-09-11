import flet as ft
from .severs import Servers
from .all_stations import AllStations
from .snackbar import Snackbar

class DDComponents:
    def __init__(self, page, on_radio_change=None):
        self.server_value = None
        self.tag_value = None
        self.radio_value = None
        self.radios = None
        self.on_radio_change = on_radio_change
        self.page = page
        self.coutrntry_codes = None

        self.ddServer = ft.DropdownM2(
            on_change=self.server_change,
            width=300,
            hint_text="Select Server",
            border_color=ft.Colors.RED,
            options=[],
        )

        self.ddGenre = ft.DropdownM2(
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
        
        self.ddCountry = ft.DropdownM2(
            width=300,
            hint_text="Select Country",
            border_color=ft.Colors.RED,
            options=[
                # ft.dropdown.Option("BG"),
                # ft.dropdown.Option("US"),
                # ft.dropdown.Option("AK"),
            ],
        )
        
        self.ddRadio = ft.DropdownM2(
            on_click=self.on_radio_click,
            on_change=self.radio_change,
            width=300,
            border_color=ft.Colors.RED,
            hint_text="Select Radio",
            options=[],
        )

        # Initialize server options
        hosts = Servers().get_radiobrowser_base_urls()
        for host in hosts:
            self.ddServer.options.append(ft.dropdown.Option(host))

    async def server_change(self, e):
        self.server_value = e.control.value
        print(f"Selected server: {self.server_value}")


        self.coutrntry_codes = await AllStations(self.server_value, self.tag_value, self.coutrntry_codes).fetch_country_codes()
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
                # Get stations for the selected server
                
                self.radios = await AllStations(self.server_value, self.tag_value, self.coutrntry_codes).get_all_stations()
                
                
                
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
                self.radios = await AllStations(self.server_value, self.tag_value, self.coutrntry_codes).get_all_stations()
                
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
        print(f"Selected radio: {self.radio_value}")
        if self.on_radio_change:
            self.on_radio_change(self.radio_value)

    async def on_radio_click(self, e):
        print("Radio dropdown focused")
        self.page.update()

    async def set_countruy_codes(self, country_codes):
        #print(self.coutrntry_codes)
        self.ddCountry.options.clear()
        for code in country_codes:
            self.ddCountry.options.append(ft.dropdown.Option(code))
        self.ddCountry.update()



           
