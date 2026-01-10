import flet as ft
import asyncio
from global_model import GlobalModel
from snackbar import Snackbar
import requests
import base64
from eq import EQ


class AudioPlayer:

    async def favorite_async_handler(self, e):
        """Direct async handler"""
        await self.update_favorite(e)
    def __init__(self, page: ft.Page, reset_listeners=None, favorite_status=None):
        print("Initializing AudioPlayer")
        
        self.page = page
        self.state = True
        self.reset_listeners = reset_listeners
        self._eq = None  # Lazy-load EQ instance
        
        self.btn_favorite = ft.IconButton(
            icon=ft.Icons.FAVORITE_BORDER,
            icon_color=ft.Colors.BLACK,
            tooltip="Add to favorites",
            disabled=True,
            on_click=self.favorite_async_handler
            # on_click=lambda e: asyncio.create_task(self.update_favorite(e, data=self.audio1.src)),

        )
        self.track_name = ft.Text("Select a station", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        self.track_artist = ft.Text("No station selected", color=ft.Colors.BLACK)
        self.leading_content = ft.Container(content= ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED))

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
        # print([self.src, self.state])
        self.main_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            # ft.Image(
                            #     src=f"/images/Weathered Chevron with Spikes and Chains.png", #"/icons/arrow_circle_up_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.png",
                            #     width=50,
                            #     height=50,
                            # ),
                            self.favicon,
                            #   ft.Image(
                            #     src=f"/images/Weathered Chevron with Spikes and Chains.png", #"/icons/arrow_circle_up_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.png",
                            #     height=50,
                            #   )
                                ], 
                                alignment=ft.MainAxisAlignment.CENTER, 
                                spacing=21
                                ),
                    # ft.Divider(),
                    ft.Row(
                        controls=[     
                            ft.ListTile(
                                leading=self.leading_content,
                                # leading=self.get_eq(),
                                title=self.track_name,
                                subtitle=self.track_artist,
                                # trailing=self.get_eq(),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=0
                    ),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            self.btn_play,
                            self.volume_icon,
                            self.slider,
                            self.btn_favorite
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10
                    ),
                ],
                spacing=10
            ),
            border=ft.border.all(3, ft.Colors.BLACK),
            border_radius=ft.border_radius.all(10),
            width=350,
            padding=ft.padding.only(left=10, top=10, right=1, bottom=13),
            image=ft.DecorationImage(
                src=f"/Weathered Chevron with Spikes and Chains.png", 
                fit=ft.ImageFit.COVER,
                opacity=0.3 
        )
            
        )

        self.audio_player = ft.Container(
             ft.Column(
                 controls=[
                     self.main_content, 
                 ], 
             ),
        )
        # self.reset_player_state()
    
    def get_eq(self):
        """Lazy-load and return a single EQ instance."""
        if self._eq is None:
            # Create a compact EQ for use in the player trailing slot
            self._eq = EQ(
                self.page,
                width=54,
                height=40,
                num_bars=6,
                levels=21,
                block_height=1,
                spacing=0,
                update_interval=0.12,
            )

            # Ensure animation is started when we create the EQ.
            try:
                # Prefer the EQ's helper which sets is_running and tries to schedule a task
                self._eq.start_animation()
            except Exception:
                pass

            # If we are already on a running loop, make sure the animation coroutine is scheduled
            try:
                import asyncio
                loop = asyncio.get_running_loop()
                if not hasattr(self._eq, "animation_task") or self._eq.animation_task is None or self._eq.animation_task.done():
                    self._eq.animation_task = loop.create_task(self._eq.equalizer_animation())
            except RuntimeError:
                # No running loop available right now; the EQ.start_animation() call
                # will attempt to schedule once the page's loop is active.
                pass

            # Update the EQ control so initial rendering happens.
            try:
                self._eq.update()
            except Exception:
                pass
    
        return self._eq
             

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

            eq_instance = self.get_eq()
                    # Place the EQ instance inside the existing leading Container's content
            try:
                self.leading_content.content = eq_instance
                        # ensure the container and eq redraw
                try:
                    self.leading_content.update()
                except Exception:
                    pass
                try:
                    eq_instance.update()
                except Exception:
                    pass
            except Exception:
                        # Fallback: replace attribute (less ideal)
                    self.leading_content = eq_instance

            self.audio1.play()
            self.audio1.update()
            self.page.update()
        elif self.state == False:
            if self.track_name:
                self.track_name.value = "Paused:"

                try:
                    self.leading_content.content = ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED)
                    # ensure the container and eq redraw
                    try:
                        self.leading_content.update()
                    except Exception:
                        pass
                    try:
                        self.leading_content.update()
                    except Exception:
                        pass
                except Exception:
                    # Fallback: replace attribute (less ideal)
                    self.leading_content.content = ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, color=ft.Colors.RED)
       
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
        try:
            # print(f"Updating title to: {radio_name}")
            
            # Ъпдейтваме текстовете
            if self.track_name:
                self.track_name.value = "Now playing:"
            
            if self.track_artist:
                self.track_artist.value = radio_name
                if len(self.track_artist.value) > 37:
                    self.track_artist.value = self.track_artist.value[:35] + "..."
                    self.leading_icon = self.get_eq()
                    print(self.leading_icon)
                
            await self.get_favicon(favicon)   
            if hasattr(self, 'page') and self.page:
                self.page.update()
                
        except Exception as ex:
            print(f"Error updating title: {ex}")


    async def update_favorite(self, e, data=None):
        print(f"update_favorite called with data: {data}")
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
    


    async def get_favicon(self, favicon=None):
        # print(f"Current favicon src: {self.favicon.src}")
        if not favicon or favicon in [None, "None", ""]:
            print("No favicon provided, setting to default.")
            self.favicon.src = f"/Weathered Chevron with Spikes and Chains.png"
            self.favicon.update()
            self.page.update()
            return
        if favicon:
            print(f"Updating favicon to: {favicon}")
            print(f"favicon value: {favicon}")
            response = requests.get(f"{favicon}")
            print(response.status_code)
            if response.status_code in [200, 201, 304]:
                favicon_data = response.content
                self.favicon.src = "data:image/jpeg;base64," + base64.b64encode(favicon_data).decode()
                self.favicon.update()
                self.page.update()
                # print(f"Updated favicon to: {self.favicon.src}")
            else:
                print(f"Failed to fetch favicon from {favicon}")
    # def reset_player_state(self):
    #     """Reset all player states to default"""
    #     self.state = True  # Stopped state
    #     self.track_name.value = "Select a station"
    #     self.track_artist.value = "No station selected"
    #     self.btn_play.icon = ft.Icons.PLAY_CIRCLE
    #     self.btn_play.tooltip = "Select a station first"
    #     self.btn_favorite.icon = ft.Icons.FAVORITE_BORDER
    #     self.btn_favorite.tooltip = "Add to favorites"
    #     self.btn_favorite.disabled = True
    #     self.slider.value = 50
    #     self.audio1.src = "empty"
    #     self.audio1.autoplay = False
    #     self.audio1.volume = 0.5
        
    #     # Reset favicon to default
    #     self.favicon.src = f"/Weathered Chevron with Spikes and Chains.png"
        
    #     # Reset leading content to music icon
    #     self.leading_content.content = ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED)
        
    #     # Stop any playing audio
    #     try:
    #         self.audio1.pause()
    #     except:
    #         pass

        

            
        
