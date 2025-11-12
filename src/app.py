import flet as ft
from appbar import AppBar
from bottom_appbar import BottomAppBar
from drop_downs import DDComponents
from global_model import GlobalModel
import asyncio
from audio_p import AudioPlayer
from audio_p import AudioPlayer
from datetime import datetime
from querys import query_radios
from version import version

print(version)

async def main(page: ft.Page):
    platform = page.platform
    print(f"Running on platform: {platform}")
    page.title = "DropDown Radio"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 8
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
    def on_scroll_top(e):
        # Scroll the page to the top
        e.page.scroll_to(offset=0, duration=500)      
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
        
    async def set_play_from_list(e):
        try:
            radio_url = e.control.data["url"]
            radio_name = e.control.data["name"]
            favicon = e.control.data.get("favicon_url")
            favorite = e.control.data.get("favorite")
            
            if radio_url:
                ap.btn_play.disabled = False
                ap.btn_play.tooltip="Play/Pause"
                ap.slider.disabled = False
                ap.btn_favorite.disabled = False
                ap.btn_play.update()
                ap.slider.update()
                ap.btn_favorite.update()

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
                
                favorite_status = favorite if favorite == True else False          
                ap.audio1.src = radio_url
                ap.audio1.autoplay = True               

                if ap.state==True:
                    print(f"Playing1:{ap.state}")          
                    ap.state = False
                    ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE
                    # e.control.icon = ft.Icons.PAUSE_CIRCLE
                    # e.control.update()   
                    # await ap.update_title_on_player("Select a station", favicon, favorite_status)    
                    ap.audio1.play()
                    ap.audio1.update()
                    page.update()   
                elif ap.state==False:
                    print(f"Paused1:{ap.state}")
                    ap.state = True
                    ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE
                    # e.control.icon = ft.Icons.PLAY_CIRCLE_FILL             
                    # favicon = ft.Image(
                    #     src=f"/Distressed Metal Chevron with Chains.png",
                    #     width=90,
                    #     height=90,
                    #     fit=ft.ImageFit.CONTAIN,
                    # )
                    await ap.update_title_on_player("Select a station", favicon, favorite_status)
                    ap.audio1.src = radio_url
                    ap.audio1.autoplay = True                   
                    # reset_listeners()
                    # e.control.update()
                    ap.audio1.play()
                    ap.audio1.update()
                    page.update()
                    # return
                # else:
                #     ap.state = False
                #     print(f"Resumed1:{ap.state}")
                #     ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE
                #     # e.control.icon = ft.Icons.PAUSE_CIRCLE
                #     # e.control.update()
                #     ap.audio1.resume()
                #     ap.audio1.update()
                #     page.update()           
                   
                await ap.update_title_on_player(radio_name, favicon, favorite_status)          
                page.update()
                # print(f"Now playing: {radio_name}")
                
        except Exception as ex:
            print(f"Error changing radio: {ex}")
    async def set_state_to_now_playing_via_dd(radio_url=None, radio_name=None, favicon=None):

        try:
            # print(f"Loading: {radio_name} - {radio_url}")
            if radio_url:
                
                ap.btn_play.disabled = False
                ap.btn_play.tooltip="Play/Pause"
                ap.slider.disabled = False
                ap.btn_favorite.disabled = False
                ap.btn_play.update()
                ap.slider.update()
                ap.btn_favorite.update()
                # if ap.audio1:
                #     ap.audio1.pause()
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
                await ap.update_title_on_player(radio_name, favicon, favorite_status)          
                page.update()
                print(f"Now playing: {radio_name}")
                
        except Exception as ex:
            print(f"Error changing radio: {ex}")
    def reset_listeners():
        print("Resetting listeners")
        # Reset all icons
        for control in last_visited_list_container.content.controls:
            # control is a ListTile, its leading is the IconButton
            if hasattr(control, 'leading') and isinstance(control.leading, ft.IconButton):
                control.leading.icon = ft.Icons.PLAY_CIRCLE_FILL
                control.leading.update()
    favorite_status = False
    ap = AudioPlayer(page=page, reset_listeners=reset_listeners, favorite_status=favorite_status)
    # def toggle_mode():
    #     print ("Toggling mode")
    dd_instance = DDComponents(page=page, on_radio_change=on_radio_change)
    global_model = GlobalModel()
    
    
    def toggle_dark_mode(e):
        dds = [dd_instance.ddServer, dd_instance.ddGenre, dd_instance.ddCountry, dd_instance.ddRadio]
        if page.theme_mode == "dark":
            dd_instance.toggle_border_color(page, self=None, e=None, dds=dds)

            licence_text.content.color = ft.Colors.WHITE
            licence_text.content.color = ft.Colors.BLACK
            page.theme_mode = "light"     
        else: 
            dd_instance.toggle_border_color(page, self=None, e=None, dds=dds)
            page.theme_mode = "dark"
            licence_text.content.color = ft.Colors.WHITE
        page.update()
        
    
    appbar = AppBar(page=page, toggle_dark_mode=toggle_dark_mode)
    page.appbar = appbar
    
    last_visited_radios = [] 
    query = query_radios["all_radios"]
    try:
        last_visited_radios = await global_model.execute_query_all(query)
        # print("Database query result:", last_visited_radios)
    except Exception as e:
        print("Database query failed:", e)
        
    

    # version = os.getenv("GITHUB_RUN_NUMBER", "0")
    # version = int(version)
    # new_version = version + 1
    # new_version = str(new_version)
    # result_version = f"{new_version[:1]}.{new_version[1:2]}.{new_version[2:3]}"
    # build_version = f"{result_version}-build.{datetime.now():%Y%m%d%H%M}"
    # info = f"© {datetime.now().year} Plambe. All rights reserved.\nVersion {build_version}"

    licence_text = ft.Column(
        controls=[
            ft.Text(
    value=f"{version}",
    size=12,
    color=ft.Colors.BLACK if page.platform == ft.PagePlatform.WINDOWS else ft.Colors.BLACK,
    text_align=ft.TextAlign.CENTER,
    weight=ft.FontWeight.BOLD,
), ft.Text(
    value="©Plambe. All rights reserved.",
    size=12,
    color=ft.Colors.BLACK if page.platform == ft.PagePlatform.WINDOWS else ft.Colors.BLACK,
    text_align=ft.TextAlign.CENTER,
    weight=ft.FontWeight.BOLD,
),
    ], alignment=ft.MainAxisAlignment.START
    )
    
    last_visited_list = ft.ListView(
    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    controls=[
        item for radio in last_visited_radios
        for item in [
            
            ft.ListTile(
                title=ft.Text(radio["name"], size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                subtitle=ft.Text(radio["url"], size=10, color=ft.Colors.WHITE, selectable=True),
                leading=ft.Image(
                    src=radio["favicon_url"] if radio["favicon_url"] not in [None, "None", ""] else f"/Weathered Chevron with Spikes and Chains.png",  
                    width=70,
                    height=70,
                ),
                trailing=ft.Icon(
                    "favorite" if radio["favorite"] else "favorite_border",
                    tooltip="Added to favorites" if radio["favorite"] else "",
                    color=ft.Colors.WHITE,
                ),     
                tooltip="Play this radio",               
                data=radio,
                on_click=lambda e: asyncio.run(set_play_from_list(e))
            ),
            ft.Divider(height=1, color=ft.Colors.WHITE),
        ]
    ][:-1],  # Remove the last divider
    height=600,
    spacing=0,
)
        # on_scroll=lambda e: on_scroll(e),
    
    last_visited_list_container = ft.Container(
        content=last_visited_list,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10),
        width=666,
        expand=True,
        height=666,
        bgcolor="#B00020",
    )

    main_column = ft.Column(

            controls=[
                ft.Container(
                    height=10
                ),
              
                        dd_instance.ddServer,
                        dd_instance.ddGenre,
                        dd_instance.ddCountry,
                        dd_instance.ddRadio,
                        
          
                ft.Text("Audio Controls", size=16, weight=ft.FontWeight.BOLD),
                ap.audio_player,
                ft.Text("Last Visited Radios", size=16, weight=ft.FontWeight.BOLD),
                last_visited_list_container,
                # licence_text, 
                BottomAppBar(licence_text=licence_text, on_scoll_to_top=on_scroll_top),
                
                # ft.Container(height=8)  # Spacer at the bottom
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
   
        )
    
    
    
 

    page.add(main_column)
    
    

