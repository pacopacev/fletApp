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
    
    ap = AudioPlayer(page=page)

    
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
    page.app = True
    page.title = "DropDown Radio"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.auto_scroll = True
    page.scroll = ft.ScrollMode.AUTO

    def on_radio_change(value, key, text, favicon):
        # print("Radio dropdown changed")
        # print(f"Key: {key}")
        # print(f"Text: {text}")
        # print(f"Radio changed to: {value}")
        ap.audio1.src = value
        ap.audio1.autoplay = True  
        try:
            if value:  
                # Ъпдейтваме аудио източника
                print(favicon)
                ap.favicon = ft.Image(
                    src=favicon if favicon else "/Distressed Metal Chevron with Chains.png",
                    width=50,
                    height=50,
                    fit=ft.ImageFit.CONTAIN
                )
                # ap.fav.src = favicon if favicon else "/Distressed Metal Chevron with Chains.png"
                ap.audio1.src = value
                ap.audio1.autoplay = True

                set_state_to_now_playing_via_dd(radio_url=key, radio_name=text, favicon=favicon)
                
                # Ъпдейтваме състоянието на бутона
                ap.state = True
                ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE
                
                
                # Ъпдейтваме UI компонентите
             
                
                # Ъпдейтваме страницата
                ap.audio1.update()
                page.update()
               
                
        except Exception as ex:
            print(f"Error changing radio: {ex}")
        
    async def set_state_to_now_playing(e,  dd_instance=None):
        

        try:
            radio_url = e.control.data["url"]
            radio_name = e.control.data["name"]
            print(f"Loading: {radio_name} - {radio_url}")

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
                
                # Ъпдейтваме аудио източника
                ap.audio1.src = radio_url
                ap.audio1.autoplay = True
                
                # Ъпдейтваме състоянието на бутона
                ap.state = True
                ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE
                
                # Ъпдейтваме UI компонентите
                await ap.update_title_on_player(radio_name)
                
                # Ъпдейтваме страницата
                page.update()
                print(f"Now playing: {radio_name}")
                
        except Exception as ex:
            print(f"Error changing radio: {ex}")

    def set_state_to_now_playing_via_dd(radio_url=None, radio_name=None, favicon=None):
        # print(favicon)
    
        try:
            # print(f"Loading: {radio_name} - {radio_url}")

            if radio_url:
                # Ако има Discord инстанция, ъпдейтваме статуса
                # if dd_instance:
                #     await dd_instance.set_now_playing(radio_name)
                
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
                
                # Ъпдейтваме аудио източника
                ap.audio1.src = radio_url
                ap.audio1.autoplay = True
                
                # Ъпдейтваме състоянието на бутона
                ap.state = True
                ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE
                
                # Ъпдейтваме UI компонентите
                ap.update_title_on_player(radio_name)
                
                # Ъпдейтваме страницата
                page.update()
                print(f"Now playing: {radio_name}")
                
        except Exception as ex:
            print(f"Error changing radio: {ex}")


    dd_instance = DDComponents(page=page, on_radio_change=on_radio_change)


    # UI Layout
    appbar = AppBar()
    page.add(appbar)

    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Image(src=f"/images/Weathered Chevron with Spikes and Chains.png"), 
                            ft.Text("Radio DropDown", size=20, weight="bold"), 
                            ft.Image(src=f"images/Weathered Chevron with Spikes and Chains.png")
                        ]
                    ),
                    padding=10,
                    border_radius=ft.border_radius.all(10),
                    alignment=ft.alignment.center,
                    width=300,
                    height=60,
                ),dd_instance.ddServer,
                dd_instance.ddGenre,
                dd_instance.ddCountry,
                dd_instance.ddRadio, 
            ]
        ),dd_instance.now_playing_container,
    )
    
    global_model = GlobalModel()
    last_visited_radios = [] 
    query_radios =  """SELECT name,url,favorite, COUNT(*) as count FROM flet_radios
                GROUP BY name, url, favorite
                ORDER BY count DESC
                LIMIT 666;"""
    try:
        last_visited_radios = await global_model.execute_query_all(query_radios)
        #print("Database query result:", last_visited_radios)
    except Exception as e:
        print("Database query failed:", e)
        
    last_visited_list = ft.ListView(
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    

        controls=[
            
            ft.ListTile(
                title=ft.Text(radio["name"]),
                subtitle=ft.Text(radio["url"]),
                leading=ft.Icon("play_arrow", tooltip=ft.Tooltip("Play")),
                trailing=ft.Icon(
                    "favorite" if radio["favorite"] else "favorite_border",
                    tooltip="Remove from favorites" if radio["favorite"] else "Add to favorites",
                    
                    ),
                    
                data=radio,
                on_click=set_state_to_now_playing,
            )
            for radio in last_visited_radios
        ],
        height=200,
    )
    
    last_visited_list_container = ft.Container(
        content=last_visited_list,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10),
        width=500,
        height=300,
        bgcolor="#B00020",
    )
    licence_text = ft.Text(
            f"© {datetime.now().year} Plambe. All rights reserved.",
            size=12,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            
            style=ft.TextStyle(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, color=ft.Colors.BLACK26,
           
    ),
)
    
    page.add(ap.audio_player)
    
    page.add(ft.Text("Last Visited Radios", size=16, weight=ft.FontWeight.BOLD))
    page.add(last_visited_list_container)
    page.add(licence_text)

# ft.app(target=main, assets_dir="assets")