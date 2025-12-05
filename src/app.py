import flet as ft
from appbar import AppBar
# from bottom_appbar import BottomAppBar
from drop_downs import DDComponents
from global_model import GlobalModel
import asyncio
from audio_p import AudioPlayer
from datetime import datetime
from querys import query_radios
from version import version
from eq import EQ

# Global reference to the app's running asyncio loop (set inside main)
APP_MAIN_LOOP = None

# print(version)

async def main(page: ft.Page):
    # store the running event loop so thread callbacks can schedule coroutines
    global APP_MAIN_LOOP
    try:
        APP_MAIN_LOOP = asyncio.get_running_loop()
    except RuntimeError:
        APP_MAIN_LOOP = None
    platform = page.platform
    # print(f"Running on platform: {platform}")
    page.title = "DropDown Radio"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  
    page.scroll = ft.ScrollMode.AUTO
    
    

    

    def on_scroll_top(e):
        e.page.scroll_to(offset=0, duration=500)

    fab_icon = ft.Icon(name=ft.Icons.ARROW_CIRCLE_UP, color=ft.Colors.BLACK)

    floating_action_button = ft.FloatingActionButton(
                    content=fab_icon,   
                    bgcolor=ft.Colors.LIME_300,
                    on_click=on_scroll_top,
                    tooltip="Scroll to Top",
                    mini=True,
                )
    def on_scroll(e: ft.OnScrollEvent):
        # print(e.pixels)
        try:
            pixels = float(e.pixels)
        except Exception:
            return

        if pixels > 100:
            if page.floating_action_button is None:
                page.floating_action_button = floating_action_button
                page.update()
        else:
            if page.floating_action_button is not None:
                page.floating_action_button = None
                page.update()
       
        
    page.on_scroll = on_scroll
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
                    print(f"Playing from list:{ap.state}")          
                    ap.state = False
                    ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE


                    eq_instance = ap.get_eq()
                    # Place the EQ instance inside the existing leading Container's content
                    try:
                        ap.leading_content.content = eq_instance
                        # ensure the container and eq redraw
                        try:
                            ap.leading_content.update()
                        except Exception:
                            pass
                        try:
                            eq_instance.update()
                        except Exception:
                            pass
                    except Exception:
                        # Fallback: replace attribute (less ideal)
                        ap.leading_content = eq_instance




                    ap.audio1.play()
                    ap.audio1.update()
                    page.update()   
                elif ap.state==False:
                    print(f"Paused1:{ap.state}")
                    ap.state = True
                    ap.btn_play.icon = ft.Icons.PAUSE_CIRCLE
           
                    await ap.update_title_on_player("Select a station", favicon, favorite_status)
                    ap.audio1.src = radio_url
                    ap.audio1.autoplay = True                   
                    # reset_listeners()
                    # e.control.update()
                    ap.audio1.play()
                    ap.audio1.update()
                    page.update()       
                   
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
    dd_instance = DDComponents(page=page, on_radio_change=on_radio_change)
    global_model = GlobalModel()
    
    
        
    
    
    
    last_visited_radios = [] 
    query = query_radios["all_radios"]
    try:
        last_visited_radios = await global_model.execute_query_all(query)
        # print("Database query result:", last_visited_radios)
    except Exception as e:
        print("Database query failed:", e)

    licence_text = ft.Container(content=ft.Column(
        controls=[
            ft.Text(
    value=f"{version}",
    size=13,
    color=ft.Colors.BLACK,
    text_align=ft.TextAlign.CENTER,
    weight=ft.FontWeight.BOLD,
), ft.Text(
    value="©Plambe. All rights reserved.",
    size=13,
    color=ft.Colors.BLACK,
    text_align=ft.TextAlign.CENTER,
    weight=ft.FontWeight.BOLD,
),
    ], alignment=ft.MainAxisAlignment.START,
    spacing=1,
    ),
    alignment=ft.alignment.bottom_left,
    margin=ft.margin.only(left=10, bottom=0, top=0),
    )

    
    
    last_visited_list = ft.ListView(
    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    controls=[
        item for radio in last_visited_radios
        for item in [
            
            ft.ListTile(
                title=ft.Text(radio["name"], size=20, weight=ft.FontWeight.BOLD,  selectable=True),
                subtitle=ft.Text(radio["url"], size=10, selectable=True),
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
                on_click=lambda e: __import__('asyncio').run_coroutine_threadsafe(set_play_from_list(e), APP_MAIN_LOOP)
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
        # bgcolor="#B00020",
        border=ft.border.all(2, ft.Colors.BLACK),
    )
    bottom_divider = ft.Divider(height=1, color=ft.Colors.BLACK, leading_indent=0, trailing_indent=0)
    main_column = ft.Column(

            controls=[
                # ft.Divider(height=3, color=ft.Colors.BLACK, leading_indent=0, trailing_indent=0),
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

                bottom_divider,
                
                ft.Container(content=licence_text, height=54)  # Spacer at the bottom
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
   
        )
    
    # pass the audio player's track_name control to the AppBar so it can update colors on theme change
    appbar = AppBar(
        page=page, 
        licence_text=licence_text, 
        bottom_divider=bottom_divider, 
        floating_action_button=floating_action_button, 
        track_name_control=ap.track_name, 
        track_artist_control=ap.track_artist,
        player_border_control=ap.main_content,
        btn_play_control=ap.btn_play,
        volume_icon_control=ap.volume_icon,
        btn_favorite_control=ap.btn_favorite,
        slider_control=ap.slider,
        dropdown_control=dd_instance.dropdowns_s,
        note_in_player=ap.leading_content
)
    page.appbar = appbar
    
    
    
 

    page.add(main_column)
    
    

