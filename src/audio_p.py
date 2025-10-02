import flet as ft
from tinytag import TinyTag
from math import pi
import asyncio
from validate_radio import ValidateRadio

class AudioPlayer:
    def __init__(self, page: ft.Page):
        self.page = page
        self.track_name = ft.Text("Select a station", weight=ft.FontWeight.BOLD)
        self.track_artist = ft.Text("No station selected")
        self.favicon = ft.Image(
            src=f"/Distressed Metal Chevron with Chains.png",
            width=90,
            height=90,
            fit=ft.ImageFit.CONTAIN,
        )
        print(f"Favicon: {self.favicon.src}")
        self.state = False
        self.volume = 0.5
        self.audio1 = ft.Audio()
        
        
        self.audio1 = ft.Audio(
        src="empty",
        autoplay=False,
        volume=0.3,
        balance=0,
        #on_loaded=lambda _: print("Loaded"),
        #on_loaded= lambda e: asyncio.run(ValidateRadio().validate_stream(e)),
        on_duration_changed=lambda e: print("Duration changed:", e.data),
        on_position_changed=lambda e: print("Position changed:", e.data),
        on_state_changed=lambda e: print("State changed:", e.data),
        # on_seek_complete=lambda _: print("Seek complete"),
    )
        self.page.overlay.append(self.audio1)
        
        
        self.btn_play = ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE, icon_size=50, on_click=self.play_track
        )
        self.volume_icon = ft.Icon(name=ft.Icons.VOLUME_DOWN)
        
      
        self.audio_control_title = ft.Text("Audio Control", size=16, weight=ft.FontWeight.BOLD)
        self.main_content = ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Container(width=100, height=100), 
                        ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED),
                                    title=self.track_name,
                                    subtitle=self.track_artist,
                            
                                ),
                                ft.Row(
                                    [
                                        self.btn_play,
                                        self.volume_icon,
                                        ft.Slider(
                                            width=150,
                                            active_color=ft.Colors.WHITE60,
                                            min=0,
                                            max=100,
                                            divisions=100,
                                            value=50,
                                            label="{value}",
                                            on_change=self.volume_change,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.FAVORITE_BORDER,
                                            on_click=lambda e, data=self.audio1.src: self.add_to_favorites(data),
                                            data=self.audio1.src
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ]
                        ),
                    ]
                ),
            ),
            
            width=600,
            color=ft.Colors.ON_PRIMARY,
            height=180,
        )

        self.stack = ft.Stack(
            controls=[
                
                self.main_content,
                self.favicon
            ],
            width=500,
            height=170
            
        )

        self.audio_player = ft.Container(
             ft.Column([
                 ft.Row([
                    ft.Text("Audio Controls", size=16, weight=ft.FontWeight.BOLD),
                 ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                 ft.Row([
                     self.stack, 
                 ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
             ]), 
        )

        
    def play_track(self, e):
        global index
        global state
    
        if self.state == False:
            print(f"Playing:{self.state}")
            self.state = True
            self.btn_play.icon = ft.Icons.PAUSE_CIRCLE
            self.audio1.play()
            self.audio1.update()
            self.page.update()
        elif self.state == True:  
            print(f"Paused:{self.state}")
            self.state = False
            self.btn_play.icon = ft.Icons.PLAY_CIRCLE
            self.audio1.pause()
            self.audio1.update()
            self.page.update()
        else:  # if state=="paused"
            print(f"Resumed:{self.state}")
            self.state = True
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

    async def update_title_on_player(self, radio_name, favicon):
        try:
            # print(f"Updating title to: {radio_name}")
            
            # Ъпдейтваме текстовете
            if self.track_name:
                self.track_name.value = "Now playing:"
            
            if self.track_artist:
                self.track_artist.value = radio_name

            if self.favicon:
                print(favicon)
                self.favicon.src = favicon
            
            # Ако има страница, ъпдейтваме
            if hasattr(self, 'page') and self.page:
                self.page.update()
                
        except Exception as ex:
            print(f"Error updating title: {ex}")


    def add_to_favorites(self, e):
        print(e)
        print("Adding to favorites")


        
            
        
