import flet as ft
from appbar import AppBar
from bottom_appbar import BottomAppBar
from drop_downs import DDComponents
from global_model import GlobalModel
import asyncio
from audio_p import AudioPlayer
from audio_p import AudioPlayer
from datetime import datetime

async def main(page: ft.Page):
    
    # page.app = True
    page.title = "DropDown Radio"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    # page.auto_scroll = True
    page.scroll = ft.ScrollMode.AUTO
    page.foreground_decoration = ft.BoxDecoration(
        gradient=ft.LinearGradient(
            colors=[
                ft.Colors.with_opacity(0.2, ft.Colors.RED),
                ft.Colors.with_opacity(0.2, ft.Colors.BLUE),
            ],
            stops=[0.0, 1.0],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
        ),
        image=ft.DecorationImage(
            src="/images/Weathered Chevron with Spikes and Chains.png",
            fit=ft.ImageFit.COVER,
            opacity=0.2,
            
        ),
    )
     
    async def on_radio_change(value, key, text, favicon):
        ap.audio1.src = value
        ap.audio1.autoplay = True  
        try:
            if value:  
                ap.audio1.src = value
                ap.audio1.autoplay = True
                await set_state_to_now_playing_via_dd(radio_url=key, radio_name=text, favicon=favicon)
                ap.state = True
                ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE
                ap.audio1.update()
                page.update()
        except Exception as ex:
            print(f"Error changing radio: {ex}")
        
    async def set_state_to_now_playing(e,  dd_instance=None):
        try:
            radio_url = e.control.data["url"]
            radio_name = e.control.data["name"]
            favicon = e.control.data.get("favicon_url")
            # print(f"Loading: {radio_name} - {radio_url}")
            
            print(f"favicon exists in database: {favicon}")

            if radio_url:
                # Ако има Discord инстанция, ъпдейтваме статуса
                if radio_url:
                    # Ако има Discord инстанция, ъпдейтваме статуса
                    if dd_instance:
                        await dd_instance.set_now_playing(radio_name)
                    # Спираме текущото възпроизвеждане
                    if ap.audio1:
                        ap.audio1.pause()
                    # Ъпдейтваме заглавието и артиста
                    if ap.track_name:
                        ap.track_name.value = "Now playing:"
                    else:
                        ap.track_name = ft.Text(radio_name)
                    if ap.track_artist:
                        ap.track_artist.value = radio_name
                    else:
                        ap.track_artist = ft.Text(radio_name)
                    ap.audio1.src = radio_url
                    ap.audio1.autoplay = True
                    ap.state = True
                    ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE
                    # Update play icon in last_visited_list to pause
                    
                    await ap.update_title_on_player(radio_name, favicon)
                    page.update()
                    print(f"Now playing: {radio_name}")
        except Exception as ex:
            print(f"Error changing radio: {ex}")

    async def set_play_from_list(e):
        try:
            radio_url = e.control.data["url"]
            radio_name = e.control.data["name"]
            favicon = e.control.data.get("favicon_url")
            print(f"Loading from list: {radio_name} - {radio_url}")
            if radio_url:
                if ap.audio1:
                    ap.audio1.pause()
                if ap.track_name:
                    ap.track_name.value = "Now playing:"
                else:
                    ap.track_name = ft.Text(radio_name)
                if ap.track_artist:
                    ap.track_artist.value = radio_name
                else:
                    ap.track_artist = ft.Text(radio_name)              
                if ap.favicon:
                    ap.favicon.src = favicon
                else:
                    ap.favicon = ft.Image(
                        src=f"/Distressed Metal Chevron with Chains.png",
                        width=90,
                        height=90,
                        fit=ft.ImageFit.CONTAIN,
                    )           
                ap.audio1.src = radio_url
                ap.audio1.autoplay = True               
                ap.state = True
                ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE
            
                if hasattr(e.control, 'icon'):
                        e.control.icon = ft.Icons.PAUSE_CIRCLE 
                        e.control.update()          
                await ap.update_title_on_player(radio_name, favicon)          
                page.update()
                print(f"Now playing: {radio_name}")
                
        except Exception as ex:
            print(f"Error changing radio: {ex}")
    async def set_state_to_now_playing_via_dd(radio_url=None, radio_name=None, favicon=None):

        try:
            # print(f"Loading: {radio_name} - {radio_url}")
            if radio_url:
                if ap.audio1:
                    ap.audio1.pause()
                if ap.track_name:
                    ap.track_name.value = "Now playing:"
                else:
                    ap.track_name = ft.Text(radio_name)
                if ap.track_artist:
                    ap.track_artist.value = radio_name
                else:
                    ap.track_artist = ft.Text(radio_name)              
                if ap.favicon:
                    ap.favicon.src = favicon
                else:
                    ap.favicon = ft.Image(
                        src=f"/Distressed Metal Chevron with Chains.png",
                        width=90,
                        height=90,
                        fit=ft.ImageFit.CONTAIN,
                    )           
                ap.audio1.src = radio_url
                ap.audio1.autoplay = True               
                ap.state = True
                ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE               
                await ap.update_title_on_player(radio_name, favicon)          
                page.update()
                print(f"Now playing: {radio_name}")
                
        except Exception as ex:
            print(f"Error changing radio: {ex}")

    ap = AudioPlayer(page=page)
    dd_instance = DDComponents(page=page, on_radio_change=on_radio_change)
    global_model = GlobalModel()
    appbar = AppBar()
    page.appbar = appbar
    
    
    last_visited_radios = [] 
    query_radios =  """SELECT name,url,favorite, favicon_url, COUNT(*) as count FROM flet_radios
                GROUP BY name, url, favorite, favicon_url
                ORDER BY count DESC
                LIMIT 666;"""
    try:
        last_visited_radios = await global_model.execute_query_all(query_radios)
        # print("Database query result:", last_visited_radios)
    except Exception as e:
        print("Database query failed:", e)





# GUI components
    licence_text = ft.Container(content=ft.Text(
            f"© {datetime.now().year} Plambe. All rights reserved.",
            size=12,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            style=ft.TextStyle(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, color=ft.Colors.BLACK26,
           
    )
),    padding=10,
    )
    last_visited_list = ft.ListView(
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        controls=[
            ft.ListTile(
                title=ft.Text(radio["name"]),
                subtitle=ft.Text(radio["url"]),
                leading=ft.IconButton(
                    icon=ft.Icons.PLAY_CIRCLE_FILL,
                    style=ft.ButtonStyle(icon_size=40),
                    icon_color=ft.Colors.WHITE,
                    tooltip="Play this radio",
                    data=radio,
                    on_click=lambda e: asyncio.run(set_play_from_list(e))
                ),
                trailing=ft.Icon(
                    "favorite" if radio["favorite"] else "favorite_border",
                    tooltip="Remove from favorites" if radio["favorite"] else "Add to favorites",
                    ),                    
                data=radio,
                # on_click=set_state_to_now_playing,
            )
            for radio in last_visited_radios
        ],
        height=200,
        # on_scroll=lambda e: on_scroll(e),
        
    )
    
    last_visited_list_container = ft.Container(
        content=last_visited_list,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10),
        width=500,
        height=300,
        bgcolor="#B00020",
    )
    
    wlcome_text = ft.Row(
                        controls=[
                            ft.Image(src=f"/images/Weathered Chevron with Spikes and Chains.png", width=40, height=40), 
                            ft.Text("Radio DropDown", size=20, weight="bold"), 
                            ft.Image(src=f"/images/Weathered Chevron with Spikes and Chains.png", width=40, height=40)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
    main_column = ft.Column(

            controls=[
                ft.Container(
                    content=wlcome_text,
                    padding=25,
                    width=300,
                    # border = ft.border.all(2, ft.Colors.RED),
                    # border_radius=ft.border_radius.all(10),
                ),
                dd_instance.ddServer,
                dd_instance.ddGenre,
                dd_instance.ddCountry,
                dd_instance.ddRadio,
                ft.Container(content=ap.audio_player, padding=15, width=500),
                ft.Text("Last Visited Radios", size=16, weight=ft.FontWeight.BOLD),
                last_visited_list_container,
                licence_text, 
                
                ft.Container(height=66)  # Spacer at the bottom
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            on_scroll_interval=0,
            on_scroll=lambda e: on_scroll(e)
        )
    
    scroll_position = 0
    last_scroll_position = 0
    
    def on_scroll(e):
        print("Scroll event triggered")
        nonlocal scroll_position, last_scroll_position
        scroll_position = e.pixels
        # Hide AppBar when scrolling down
        if scroll_position > last_scroll_position + 20:
            if appbar.visible:
                appbar.visible = False
                page.update()
        # Show AppBar when scrolling up
        elif scroll_position < last_scroll_position - 20:
            if not appbar.visible:
                appbar.visible = True
                page.update()
        last_scroll_position = scroll_position

    


    
    
        
    page.add(main_column)
    
    

