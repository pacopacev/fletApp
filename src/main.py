import flet as ft
from src.appbar import AppBar
from src.bottom_appbar import BottomAppBar
from src.drop_downs import DDComponents

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="uvicorn")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="websockets")

async def main(page: ft.Page):
    page.title = "Radio Browser"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    # Define callback function for radio selection
    def on_radio_change(value):
        print(f"Radio changed to: {value}")
        audio1.src = value
        audio1.autoplay = True
        audio1.update()
        page.update()

    # Create dropdown components instance with callback
    dd_instance = DDComponents(page=page, on_radio_change=on_radio_change)

    # Audio control functions
    def volume_down(_):
        audio1.volume = max(0, audio1.volume - 0.1)
        audio1.update()

    def volume_up(_):
        audio1.volume = min(1, audio1.volume + 0.1)
        audio1.update()

    def balance_left(_):
        audio1.balance = max(-1, audio1.balance - 0.1)
        audio1.update()

    def balance_right(_):
        audio1.balance = min(1, audio1.balance + 0.1)
        audio1.update()

    def play(_):
        audio1.play()
        audio1.update()

    def pause(_):
        audio1.pause()
        audio1.update()

    def resume(_):
        audio1.resume()
        audio1.update()

    def release(_):
        audio1.release()
        audio1.update()

    def get_duration(_):
        print("Current duration:", audio1.get_duration())

    def get_position(_):
        print("Current position:", audio1.get_current_position())

    # Initialize audio player
    audio1 = ft.Audio(
        src="https://stream.radiobrowser.de/rock-128.mp3",
        autoplay=False,
        volume=0.7,
        balance=0,
        on_loaded=lambda _: print("Loaded"),
        on_duration_changed=lambda e: print("Duration changed:", e.data),
        on_position_changed=lambda e: print("Position changed:", e.data),
        on_state_changed=lambda e: print("State changed:", e.data),
        on_seek_complete=lambda _: print("Seek complete"),
    )
    page.overlay.append(audio1)

    # UI Layout
    appbar = AppBar()
    page.add(appbar)
    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("↓DropDowns Here↓", size=20, weight=ft.FontWeight.BOLD),
                    padding=10,
                    border_radius=ft.border_radius.all(10),
                    alignment=ft.alignment.center,
                    width=300,
                    height=50,
                ),dd_instance.ddServer,dd_instance.ddGenre,dd_instance.ddCountry,dd_instance.ddRadio,
            ]
        ),
        ft.Container(
            ft.Column([
                ft.Row([
                    ft.Text("Audio Controls", size=16, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                ft.Row([
                    ft.ElevatedButton("Play", on_click=play),
                    ft.ElevatedButton("Pause", on_click=pause),
                    ft.ElevatedButton("Resume", on_click=resume),
                    ft.ElevatedButton("Release", on_click=release),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                ft.Row([
                    ft.ElevatedButton("Volume -", on_click=volume_down),
                    ft.ElevatedButton("Volume +", on_click=volume_up),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                ft.Row([
                    ft.ElevatedButton("Balance ←", on_click=balance_left),
                    ft.ElevatedButton("Balance →", on_click=balance_right),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                ft.Row([
                    ft.ElevatedButton("Get Duration", on_click=get_duration),
                    ft.ElevatedButton("Get Position", on_click=get_position),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            padding=20,
            border_radius=ft.border_radius.all(10),
        )
    )

# Create FastAPI app


# For local development
ft.app(target=main, view=ft.WEB_BROWSER)