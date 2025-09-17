import flet as ft
import flet.fastapi as fastapi
from fastapi import FastAPI
from appbar import AppBar
from bottom_appbar import BottomAppBar
from drop_downs import DDComponents
import warnings
from global_model import GlobalModel
import asyncio

warnings.filterwarnings("ignore", category=DeprecationWarning, module="uvicorn")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="websockets")

# Create FastAPI app
app = FastAPI()

async def main(page: ft.Page):
    page.foreground_decoration = ft.BoxDecoration(
        gradient=ft.LinearGradient(
            colors=[
                ft.Colors.with_opacity(0.2, ft.Colors.RED),  # use lightly transparent colors instead of solid ones
                ft.Colors.with_opacity(0.2, ft.Colors.BLUE),
            ],
            stops=[0.0, 1.0],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
        ),
        image=ft.DecorationImage(
            src="Weathered Chevron with Spikes and Chains.png",
            fit=ft.ImageFit.COVER,
            opacity=0.2,
        ),
    )
    page.app = True
    page.title = "Radio Browser"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.auto_scroll = True
    page.scroll = ft.ScrollMode.AUTO
    
    # Define callback function for radio selection
    def on_radio_change(value):
        print(f"Radio changed to: {value}")
        audio1.src = value
        audio1.autoplay = True
        audio1.update()
        page.update()

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
    
    
    last_visited_radios = [
    {"name": "Metal FM", "url": "http://..."},
    {"name": "Rock Radio", "url": "http://..."},
]
    
    last_visited_list = ft.ListView(
    controls=[
        ft.ListTile(
            title=ft.Text(radio["name"]),
            subtitle=ft.Text(radio["url"]),
            leading=ft.Icon("radio"),
            trailing=ft.Icon("play_arrow"),
            # on_click=lambda e, url=radio["url"]: print(f"Clicked {url}"),
        )
        for radio in last_visited_radios
    ],
    height=200,  # adjust as needed
)
    last_visited_list_container = ft.Container(
            content=last_visited_list,
            alignment=ft.alignment.center,
            border_radius=ft.border_radius.all(10),
            width=400,
            height=220,
            bgcolor="#B00020",
        )
    
    page.add(ft.Text("Last Visited Radios", size=16, weight=ft.FontWeight.BOLD))
    page.add(last_visited_list_container)
    
    
    # Database test
    global_model = GlobalModel()
    test = []
    try:
        test = await global_model.execute_query_all("SELECT * FROM users LIMIT 10;")
        # print("Database query result:", test)
    except Exception as e:
        print("Database query failed:", e)



    
    
    



ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="assets")