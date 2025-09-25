import flet as ft
from tinytag import TinyTag
from math import pi

class AudioPlayer:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state = False
        self.volume = 0.5
        # self.audio_init = TinyTag.get(page.overlay[index].src)
        self.current_time = ft.Text(value="0:0")
        # self.remaining_time = ft.Text(value=self.converter_time(self.audio_init.duration * 1000))
        # self.progress_track = ft.ProgressBar(width=400, value="0", height=8)
        # self.track_name = ft.Text(value=self.audio_init.title)
        # self.track_artist = ft.Text(value=self.audio_init.artist)
        self.track_title = ft.Text("No Track")
        
        self.audio1 = ft.Audio(
        src="https://stream.radiobrowser.de/rock-128.mp3",
        autoplay=False,
        volume=0.3,
        balance=0,
        on_loaded=lambda _: print("Loaded"),
        on_duration_changed=lambda e: print("Duration changed:", e.data),
        on_position_changed=lambda e: print("Position changed:", e.data),
        on_state_changed=lambda e: print("State changed:", e.data),
        on_seek_complete=lambda _: print("Seek complete"),
    )
        page.overlay.append(self.audio1)
        self.btn_play = ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE, icon_size=50, on_click=self.play_track
        )
        self.volume_icon = ft.Icon(name=ft.Icons.VOLUME_DOWN)
        
        self.disc_image = ft.Image(
            src="/audio_player/album.png",
            width=90,
            height=90,
            fit=ft.ImageFit.CONTAIN,
            # rotate=ft.Rotate(0, alignment=ft.alignment.center_left),
            # rotate=ft.transform.Rotate(0, alignment=ft.alignment.center),
            
        )
        # self.disc_image_container = ft.Container(
        #     content=self.disc_image,
        #     width=200,
        #     height=200,
        #     alignment=ft.alignment.center,
        #     border_radius=ft.border_radius.all(100),
        #     animate=ft.Animation(100, ft.AnimationCurve.EASE_IN_CIRC),
        # )
        self.audio_control_title = ft.Text("Audio Control", size=16, weight=ft.FontWeight.BOLD)
        self.main_content = ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Container(width=80, height=300),
                        ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED),
                                    # title=self.track_name,
                                    title=self.track_title,
                                    # subtitle=self.track_artist,
                                    subtitle=ft.Text(value="No Artist"),
                                ),
                                # ft.Row(
                                #     ["0", "0", "0"],
                                #     # [self.current_time, self.progress_track, self.remaining_time],
                                #     alignment=ft.MainAxisAlignment.END,
                                # ),
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
                # self.disc_image_container,
                self.disc_image,
            ],
            width=500,
            height=180,
            
        )

        self.audio_player = ft.Container(
             ft.Column([
                 ft.Row([
                    ft.Text("Audio Controls", size=16, weight=ft.FontWeight.BOLD),
                 ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                 ft.Row([
                     self.stack, 
                 ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
             ])
        )

        

    def converter_time(self, millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        return "%d:%d" % (minutes, seconds)
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

    async def update_title_on_player(self, radio_name):
        
        print(f"Radio changed to: {radio_name}")
        self.track_title.value = radio_name

        
            
        
