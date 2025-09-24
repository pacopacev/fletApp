import flet as ft
from tinytag import TinyTag
from math import pi

class AudioPlayer:
    def __init__(self, page: ft.Page):
        # self.audio_init = TinyTag.get(page.overlay[index].src)
        self.current_time = ft.Text(value="0:0")
        # self.remaining_time = ft.Text(value=self.converter_time(self.audio_init.duration * 1000))
        # self.progress_track = ft.ProgressBar(width=400, value="0", height=8)
        # self.track_name = ft.Text(value=self.audio_init.title)
        # self.track_artist = ft.Text(value=self.audio_init.artist)
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
                        ft.Container(width=80, height=200),
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
                                        ft.IconButton(
                                            icon=ft.Icons.SKIP_PREVIOUS,
                                            icon_size=40,
                                            on_click=self.previous_track,
                                        ),
                                        self.btn_play,
                                        ft.IconButton(
                                            icon=ft.Icons.SKIP_NEXT,
                                            icon_size=40,
                                            on_click=self.next_track,
                                        ),
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
                                            icon=ft.Icons.PLAYLIST_ADD_ROUNDED,
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
            width=680,
            height=300,
        )

    def converter_time(self, millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        return "%d:%d" % (minutes, seconds)
    def play_track(self,e):
        global index
        global state
        if state == "":
            state = "playing"
            self.btn_play.icon = ft.Icons.PAUSE_CIRCLE
            # page.overlay[index].play()
        elif state == "playing":
            state = "paused"
            self.btn_play.icon = ft.Icons.PLAY_CIRCLE
            # page.overlay[index].pause()
        else:  # if state=="paused"
            state = "playing"
            self.btn_play.icon = ft.Icons.PAUSE_CIRCLE
            # page.overlay[index].resume()
    def volume_change(self, e):
        global index
        global volume
        v = e.control.value
        # page.overlay[index].volume = 0.01 * v
        volume = 0.01 * v
        if v == 0:
            self.volume_icon.name = ft.Icons.VOLUME_OFF
        elif 0 < v <= 50:
            self.volume_icon.name = ft.Icons.VOLUME_DOWN
        elif 50 < v:
            self.volume_icon.name = ft.Icons.VOLUME_UP
        # page.update()
        
    def next_track(self, e):
        global index
        # page.overlay[index].release()
        # page.overlay[index].update()
        index = index + 1
        if index == len(page.overlay):
            index = 1
        self.new_track()
        # page.update()

    def previous_track(self, e):
        global index
        # page.overlay[index].release()
        # page.overlay[index].update()
        index = index - 1
        # if index == 0:
        #     index = len(page.overlay) - 1
        # self.new_track()
        # page.update()
        
    def new_track(self):
        global index
        global state
        global volume
        self.disc_image.rotate.angle += pi * 2
        # audio = TinyTag.get(page.overlay[index].src)
        # self.track_name.value = audio.title
        # self.track_artist.value = audio.artist
        self.current_time.value = "0:0"
        # self.remaining_time.value = self.converter_time(audio.duration * 1000)
        self.progress_track.value = "0"
        #if state == "playing":
            # page.overlay[index].volume = volume
            # page.overlay[index].play()