import flet as ft

class AudioPlayer:
    def __init__(self):
        self.player = ft.Audio(
            src="https://stream.radiobrowser.de/rock-128.mp3",
            autoplay=False,
            volume=0.5,
            balance=0.0,
            on_loaded=lambda _: print("Loaded"),
            on_duration_changed=lambda e: print("Duration changed:", e.data),
            on_position_changed=lambda e: print("Position changed:", e.data),
            on_state_changed=lambda e: print("State changed:", e.data),
            on_seek_complete=lambda _: print("Seek complete"),
            # on_error=self.on_error,
            #on_complete=self.on_complete,
        )
        self.is_playing = False

    def play(self, url):
        self.player.src = url
        self.player.autoplay = True
        self.is_playing = True
        self.player.update()

    def pause(self):
        if self.is_playing:
            self.player.pause()
            self.is_playing = False
            self.player.update()

    def resume(self):
        if not self.is_playing:
            self.player.play()
            self.is_playing = True
            self.player.update()

    def release(self):
        self.player.src = ""
        self.is_playing = False
        self.player.update()

    def volume_up(self):
        if self.player.volume < 1.0:
            self.player.volume = min(1.0, self.player.volume + 0.1)
            self.player.update()

    def volume_down(self):
        if self.player.volume > 0.0:
            self.player.volume = max(0.0, self.player.volume - 0.1)
            self.player.update()

    def balance_left(self):
        if self.player.balance > -1.0:
            self.player.balance = max(-1.0, self.player.balance - 0.1)
            self.player.update()

    def balance_right(self):
        if self.player.balance < 1.0:
            self.player.balance = min(1.0, self.player.balance + 0.1)
            self.player.update()

    # def on_error(self, e):
    #     print(f"Audio error: {e}")

    # def on_complete(self, e):
    #     print("Audio playback completed")
    #     self.is_playing = False
    #     self.player.update()