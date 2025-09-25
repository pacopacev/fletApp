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
        
        self.audio1 = ft.Audio(
        src="https://stream.radiobrowser.de/rock-128.mp3",
        autoplay=False,
        volume=0.5,
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
            width=100,
            height=100,
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
                                    title=ft.Text(value="No Track"),
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
                                        # ft.IconButton(
                                        #     icon=ft.Icons.SKIP_PREVIOUS,
                                        #     icon_size=40,
                                        #     on_click=self.previous_track,
                                        # ),
                                        self.btn_play,
                                        # ft.IconButton(
                                        #     icon=ft.Icons.SKIP_NEXT,
                                        #     icon_size=40,
                                        #     on_click=self.next_track,
                                        # ),
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
                                            # on_click=lambda _: pick_files_dialog.pick_files(
                                            #     allow_multiple=True,
                                            #     file_type=ft.FilePickerFileType.AUDIO,
                                            # ),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ]
                        ),
                    ]
                ),
            ),
            
            width=580,
            color=ft.Colors.ON_PRIMARY,
            height=180,
        )

        self.stack = ft.Stack(
            controls=[
                self.main_content,
                # self.disc_image_container,
                self.disc_image,
            ],
            width=600,
            height=300,
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
        
    # def next_track(self, e):
    #     global index
    #     # page.overlay[index].release()
    #     # page.overlay[index].update()
    #     index = index + 1
    #     if index == len(page.overlay):
    #         index = 1
    #     self.new_track()
    #     # page.update()

    # def previous_track(self, e):
    #     global index
    #     # page.overlay[index].release()
    #     # page.overlay[index].update()
    #     index = index - 1
    #     # if index == 0:
    #     #     index = len(page.overlay) - 1
    #     # self.new_track()
    #     # page.update()
        
    # def new_track(self):
    #     global index
    #     global state
    #     global volume
    #     self.disc_image.rotate.angle += pi * 2
    #     # audio = TinyTag.get(page.overlay[index].src)
    #     # self.track_name.value = audio.title
    #     # self.track_artist.value = audio.artist
    #     self.current_time.value = "0:0"
    #     # self.remaining_time.value = self.converter_time(audio.duration * 1000)
    #     self.progress_track.value = "0"
    #     #if state == "playing":
    #         # page.overlay[index].volume = volume
    #         # page.overlay[index].play()