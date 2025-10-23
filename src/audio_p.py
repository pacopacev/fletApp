import flet as ft
import asyncio
from global_model import GlobalModel
from snackbar import Snackbar


class AudioPlayer:
    def __init__(self, page: ft.Page, reset_listeners=None, favorite_status=None):
        self.page = page
        self.reset_listeners = reset_listeners
        # self.add_to_favorites = add_to_favorites
        self.btn_favorite = ft.IconButton(
            icon=ft.Icons.FAVORITE_BORDER,
            icon_color=ft.Colors.BLACK,
            tooltip="Add to favorites",
            disabled=True,
            on_click=lambda e: asyncio.run(self.update_favorite(e, data=self.audio1.src)),
        )
        self.track_name = ft.Text("Select a station", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        self.track_artist = ft.Text("No station selected", max_lines=4, overflow="ellipsis", color=ft.Colors.BLACK)
        self.favicon = ft.Image(
            src=f"/Distressed Metal Chevron with Chains.png",
            width=90,
            height=90,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(10)
        )
        
        self.slider = ft.Slider(
                                            width=150,
                                            thumb_color=ft.Colors.BLACK,
                                            overlay_color=ft.Colors.RED,
                                            min=0,
                                            max=100,
                                            divisions=100,
                                            value=50,
                                            label="{value}",
                                            disabled=True,
                                            on_change=self.volume_change,
                                      )
        # print(f"Favicon: {self.favicon.src}")
        self.state = True
        self.volume = 0.5
        self.src = "empty"
        self.audio1 = ft.Audio()
        
        
        self.audio1 = ft.Audio(
        src=self.src,
        autoplay=False,
        volume=0.3,
        balance=0,
        #on_loaded=lambda _: print("Loaded"),
        #on_loaded= lambda e: asyncio.run(ValidateRadio().validate_stream(e)),
        # on_duration_changed=lambda e: print("Duration changed:", e.data),
        # on_position_changed=lambda e: print("Position changed:", e.data),
        # on_state_changed=lambda e: print("State changed:", e.data),
        # on_seek_complete=lambda _: print("Seek complete"),
    )
        self.page.overlay.append(self.audio1)
        
        
        self.btn_play = ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE,
            icon_color=ft.Colors.BLACK,
            icon_size=50, 
            on_click=self.play_track,
            disabled=False,
            tooltip="Select a station first"
        )
        self.volume_icon = ft.Icon(name=ft.Icons.VOLUME_DOWN, color=ft.Colors.BLACK)
        
      
        self.audio_control_title = ft.Text("Audio Control", size=16, weight=ft.FontWeight.BOLD)
        self.main_content = ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [ self.favicon,
                        # ft.Container(width=100, height=100), 
                        ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, color=ft.Colors.BLACK),
                                    title=self.track_name,
                                    subtitle=self.track_artist,
                            
                                ),
                                ft.Row(
                                    [
                                        self.btn_play,
                                        self.volume_icon,
                                        self.slider,
                                        self.btn_favorite
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ]
                        ),
                    ]
                ),
                padding=15,
                border=ft.border.all(5, ft.Colors.WHITE),
                border_radius=ft.border_radius.all(10),
            ),

        
            # width=600,
            color=ft.Colors.WHITE,
            height=180,
            variant=ft.CardVariant.OUTLINED,
        )

        self.stack = ft.Container(
            content=self.main_content,
            width=500,
            height=180
            
        )

        self.audio_player = ft.Container(
             ft.Column([
                 ft.Row([
                    ft.Text("Audio Controls", size=16, weight=ft.FontWeight.BOLD),
                 ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                 ft.Row([
                    self.stack,
                    #  self.main_content 
                 ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
             ])
        )

        
    def play_track(self, e):
        global index
        if self.audio1.src == "empty" or not self.audio1.src:
            snackbar_instance = Snackbar("No station selected", bgcolor="green", length = None)
            snackbar_instance.open = True  
            self.page.controls.append(snackbar_instance)
            self.page.update()
            return
    
        if self.state == True:
            print(f"Playing:{self.state}")
            if self.track_name:
                self.track_name.value = "Now playing:"
                
            self.state = False
            self.btn_play.icon = ft.Icons.PAUSE_CIRCLE
            self.audio1.play()
            self.audio1.update()
            self.page.update()
        elif self.state == False:
            if self.track_name:
                self.track_name.value = "Paused:"
            # self.reset_listeners()
            print(f"Paused:{self.state}")
            self.state = True
            self.btn_play.icon = ft.Icons.PLAY_CIRCLE
            self.audio1.pause()
            self.audio1.update()
            self.page.update()
        else:  # if state=="paused"
            print(f"Resumed:{self.state}")
            if self.track_name:
                self.track_name.value = "Now playing:"
            self.state = False
            self.btn_play.icon = ft.Icons.PAUSE_CIRCLE
            self.audio1.resume()
            self.audio1.update()
            self.page.update()

    def volume_change(self, e):
        global volume
        
        if 'volume' not in globals():
            volume = 0  # or whatever default value you want
        v = e.control.value
        
        # Store the previous volume for comparison
        previous_volume = volume
        
        # Convert slider value (0-100) to audio volume (0.0-1.0)
        volume = v / 100.0
        
        # Update the audio volume directly
        self.audio1.volume = volume
        
        # Update volume icon based on slider position
        if v == 0:
            self.volume_icon.name = ft.Icons.VOLUME_OFF
        elif 0 < v <= 50:
            self.volume_icon.name = ft.Icons.VOLUME_DOWN
        else:  # v > 50
            self.volume_icon.name = ft.Icons.VOLUME_UP
        
        # Optional: Print direction of change (if needed for debugging)
        if v > previous_volume * 100:  # Convert back for comparison
            print("Volume up")
        elif v < previous_volume * 100:
            print("Volume down")
        
        self.page.update()

    async def update_title_on_player(self, radio_name, favicon, favorite_status):
        self.btn_favorite.icon = ft.Icons.FAVORITE_BORDER
        self.btn_favorite.update()
        # print(favorite_status)
        
        # self.btn_favorite.icon = ft.Icons.FAVORITE if favorite_status == True else ft.Icons.FAVORITE_BORDER
        # self.btn_favorite.icon = ft.Icons.FAVORITE_BORDER
        # self.btn_favorite.update()
        try:
            # print(f"Updating title to: {radio_name}")
            
            # Ъпдейтваме текстовете
            if self.track_name:
                self.track_name.value = "Now playing:"
            
            if self.track_artist:
                self.track_artist.value = radio_name

            if favicon:
                print(f"Updating favicon to: {favicon}")
                self.favicon.src = favicon
                self.favicon.update()
                self.page.update()
            else:
                self.favicon.src = f"/Weathered Chevron with Spikes and Chains.png"
                self.favicon.update()
                self.page.update()
                
            # if favorite_status == True:
            #     self.btn_favorite.icon = ft.Icons.FAVORITE
            #     self.btn_favorite.update()
            #     self.page.update()
            # else:
            #     self.btn_favorite.icon = ft.Icons.FAVORITE_BORDER
            #     self.btn_favorite.update()
            #     self.page.update()
            
            # Ако има страница, ъпдейтваме
            if hasattr(self, 'page') and self.page:
                self.page.update()
                
        except Exception as ex:
            print(f"Error updating title: {ex}")


    async def update_favorite(self, e, data=None):
        # Use the current audio source or provided data
        station_url = self.audio1.src if self.audio1.src else False
        station_name = self.track_artist.value
        print(f"Updating favorite: {station_name} - {station_url}")
        status_favorite = True
        status_update = await GlobalModel().execute_query_update(
            table="flet_radios",
            columns=("favorite",),
            updates=(status_favorite,),
            where=(("url", station_url),)
        
        )
        # print(status_update)
        if status_update != True:
            print(f"Failed to update favorite status for {station_name}")
        else:
            if self.btn_favorite.icon == ft.Icons.FAVORITE:
                self.btn_favorite.icon = ft.Icons.FAVORITE_BORDER
                
                self.btn_favorite.update()
                await self.remove_favorite(station_url)
            else:
                self.btn_favorite.icon = ft.Icons.FAVORITE
                self.btn_favorite.tooltip = "Added to favorites"
                snackbar_instance = Snackbar("Added to favorites", bgcolor="green", length = None)
                snackbar_instance.open = True  
                self.page.controls.append(snackbar_instance)
                self.page.update()
            

            print(f"Successfully updated favorite status for {station_name}")


    async def remove_favorite(self, station_url):
        status_favorite = False
        status_update = await GlobalModel().execute_query_update(
            table="flet_radios",
            columns=("favorite",),
            updates=(status_favorite,),
            where=(("url", station_url),)
        )
        try:
            if status_update != True:
                print(f"Failed to remove favorite status for URL: {station_url}")
            else:
                print(f"Successfully removed favorite status for URL: {station_url}")
                snackbar_instance = Snackbar("Removed from favorites", bgcolor="green", length = None)
                snackbar_instance.open = True  
                self.page.controls.append(snackbar_instance)
                self.page.update()
        except Exception as e:
            print(f"Error in remove_favorite: {e}")
        return status_update
    
    async def set_to_default(self):
        self.track_name.value = "Select a station"
        self.track_name.update()
        self.track_artist.value = "No station selected"
        self.track_artist.update()
        self.favicon.src = f"/Distressed Metal Chevron with Chains.png"
        self.favicon.update()
        self.page.update()        
        
        
 
      


        
            
        
