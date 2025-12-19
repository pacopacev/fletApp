import flet as ft
import os
from info_banner import InfoDialog
from submit_bug import SubmitBug

class AppBar(ft.AppBar):
    def __init__(self, 
                 page, 
                 licence_text, 
                 bottom_divider, 
                 floating_action_button, 
                 track_name_control=None, 
                 track_artist_control=None,
                 player_border_control=None, 
                 btn_play_control=None, 
                 volume_icon_control=None,
                 btn_favorite_control=None,
                 slider_control=None,
                 dropdown_control=None,
                 note_in_player=None,
                 last_visited_list_border=None,):
        self.page = page
        self.licence_text = licence_text
        self.bottom_divider = bottom_divider
        self.floating_action_button = floating_action_button
        # optional reference to the main audio player's track name control
        self.track_name_control = track_name_control
        self.track_artist_control = track_artist_control
        self.player_border_control = player_border_control
        self.btn_play_control = btn_play_control
        self.volume_icon = volume_icon_control
        self.btn_favorite_control = btn_favorite_control
        self.slider_control = slider_control    
        self.dropdown_control = dropdown_control
        self.note_in_player = note_in_player
        self.last_visited_list_border = last_visited_list_border
        
        if os.getenv("PUBLIC_URL"):
            self.public_url = os.getenv("PUBLIC_URL", "http://127.0.0.1:8000/")
        super().__init__(
            leading=ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.HOME,
                    tooltip="Go to main page",
                    on_click=lambda _: self.page.launch_url(self.public_url),
                ),
                # content=ft.Image(
                # src=f"/Distressed Metal Chevron with Chains.png", 
                # # width=30, 
                # # height=30,
                # tooltip=ft.Tooltip("Go to main page"),
                # ), 
                #  on_click=lambda _: self.page.launch_url("http://127.0.0.1:8553/"),
                               
            ),
            toolbar_height=50,

            # leading=ft.Container(width=40, height=40),
            leading_width=50,
            title=ft.Row(
                controls=[
                     ft.Image(src=f"/images/Weathered Chevron with Spikes and Chains.png", width=40, height=40), 
                     ft.Text("Radio DropDown", size=20, weight="bold"), 
                     ft.Image(src=f"images/Weathered Chevron with Spikes and Chains.png", width=40, height=40)
                ],
                alignment="center"
            ),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(
                        content=ft.Row(
                    [
                        ft.Icon(ft.Icons.LINK),
                        ft.Text("Try on deprecated website"),
                    ]
                ),
                     
                        tooltip="Try on deprecated website", 
                        mouse_cursor=ft.MouseCursor.CLICK,
                        checked=False, 
                        on_click=lambda _: self.page.launch_url("https://plambe.wuaze.com")
                    ),
                    
                    ft.PopupMenuItem(),
                    
                    ft.PopupMenuItem(
                        content=ft.Row(
                    [
                        ft.Icon(ft.Icons.WB_SUNNY_OUTLINED),
                        ft.Text("Toggle Light/Dark Mode"),
                    ]
                ),
                        checked=False, 
                        on_click=self.toggle_dark_mode
                    ),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(
                        content=ft.Row(
                    [
                        ft.Icon(ft.Icons.INFO),
                        ft.Text("Info"),
                    ]
                ),
                        checked=False, 
                        on_click=self.get_info
                    ),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(
                        content=ft.Row(
                    [
                        ft.Icon(ft.Icons.BUG_REPORT),
                        ft.Text("Report a bug"),
                    ]
                ),
                        checked=False, 
                        on_click=self.submit_bug
                    ),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(
                        content=ft.Row(
                    [
                        ft.Icon(ft.Icons.MONETIZATION_ON),
                        ft.Text("Donate"),
                    ]
                ),
                        checked=False, 
                        on_click=lambda _: self.page.launch_url("https://www.buymeacoffee.com/")
                    ),
                    
                ], padding =ft.Padding(0,0,0,0), elevation=0,
            ),
               
            ],
        )
    def get_info(self, e):
        info_banner = InfoDialog(self.page)
        info_banner.open_banner(page=self.page)
        self.page.update()
        
    def submit_bug(self, e):

        bug_report = SubmitBug(self.page)
        self.page.open(bug_report)
        self.page.update()

    
    def toggle_dark_mode(self, e):
        # Toggle between light and dark mode
        if self.page.theme_mode == "dark":
            print("Toggling to light mode")
            self.page.theme_mode = "light"
            text_color = ft.Colors.BLACK
            divider_color = ft.Colors.BLACK
            fab_icon_color = ft.Colors.BLACK
        else:
            print("Toggling to dark mode")
            self.page.theme_mode = "dark"
            text_color = ft.Colors.WHITE
            divider_color = ft.Colors.WHITE
            fab_icon_color = ft.Colors.BLACK

        # Update licence text colors if present
        try:
            col = getattr(self.licence_text, 'content', None)
            if col and hasattr(col, 'controls'):
                controls = col.controls
                if len(controls) >= 1:
                    controls[0].color = text_color
                if len(controls) >= 2:
                    controls[1].color = text_color
        except Exception:
            pass

        # Update divider color if present
        try:
            if self.bottom_divider is not None:
                self.bottom_divider.color = divider_color
        except Exception:
            pass

        # Update floating action button icon color if present
        try:
            fab = getattr(self, 'floating_action_button', None)
            if fab is not None:
                fab.icon_color = fab_icon_color
                try:
                    fab.update()
                except Exception:
                    pass
        except Exception:
            pass

        # Update track name control color if a reference was provided when AppBar was created
        try:
            if getattr(self, 'track_name_control', None) is not None:
                t = self.track_name_control
                t.color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                try:
                    t.update()
                except Exception:
                    pass
        except Exception:
            pass

        try:
            if getattr(self, 'track_artist_control', None) is not None:
                t = self.track_artist_control
                t.color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                try:
                    t.update()
                except Exception:
                    pass
        except Exception:
            pass
        try:
            if getattr(self, 'note_in_player', None) is not None:
                t = self.note_in_player
                t.color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                print("Updating note in player color")
                print(t.color)
                try:
                    t.update()
                except Exception:
                    pass
        except Exception:
            pass
        try:
            if getattr(self, 'player_border_control', None) is not None:
                b = self.player_border_control
                if hasattr(b, 'border') and b.border is not None:
                    # Reconstruct border with new color (Border objects are immutable)
                    new_color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                    old_border = b.border
                    # Preserve width and create new border with updated color
                    width = getattr(old_border, 'left', None)
                    if width and hasattr(width, 'width'):
                        width = width.width
                    else:
                        width = 3  # default fallback
                    b.border = ft.border.all(width, new_color)
                try:
                    b.update()
                except Exception:
                    pass
        except Exception:
            pass
        
        try:
            if getattr(self, 'btn_play_control', None) is not None:
                # print("Updating btn play color")
                b = self.btn_play_control
                b.icon_color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                try:
                    # print("Updating btn play color")
                    b.update()
                except Exception:
                    pass
        except Exception:
            pass
        
        try:
            if getattr(self, 'volume_icon', None) is not None:
                # print("Updating btn next color")
                b = self.volume_icon
                b.color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                try:
                    # print("Updating btn next color")
                    b.update()
                except Exception:
                    pass
        except Exception:
            pass
        
        try:
            if getattr(self, 'btn_favorite_control', None) is not None:
                # print("Updating btn next color")
                b = self.btn_favorite_control
                b.icon_color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                try:
                    # print("Updating btn next color")
                    b.update()
                except Exception:
                    pass
        except Exception:
            pass
        
        try:
            if getattr(self, 'slider_control', None) is not None:
                b = self.slider_control
                b.thumb_color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                try:
                    # print("Updating btn next color")
                    b.update()
                except Exception:
                    pass
        except Exception:
            pass
        
        try:
            if getattr(self, 'dropdown_control', None) is not None:
                for i in range(len(self.dropdown_control)):
                    b = self.dropdown_control[i]
                    b.border_color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                    b.label_style.color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                    b.trailing_icon.color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                    b.leading_icon.color = ft.Colors.WHITE if self.page.theme_mode == "dark" else ft.Colors.BLACK
                    try:
                        b.update()
                    except Exception:
                        pass
        except Exception:
            pass
        
        try:
            if getattr(self, 'last_visited_list_border', None) is not None:
                b = self.last_visited_list_border
                b.border = ft.border.all(2, ft.Colors.WHITE) if self.page.theme_mode == "dark" else ft.border.all(2, ft.Colors.BLACK)
                try:
                    b.update()
                except Exception:
                    pass
        except Exception:
            pass



        self.page.update()
        
        


