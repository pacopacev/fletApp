import flet as ft
import os
from info_banner import InfoBanner
from submit_bug import SubmitBug



class AppBar(ft.AppBar):
    def __init__(self, page, toggle_dark_mode=None):
        self.page = page
        self.toggle_dark_mode = toggle_dark_mode
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
                        # icon = ft.Icons.WB_SUNNY_OUTLINED, 
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
                    )
                ], padding =ft.Padding(0,0,0,0), elevation=0,
            ),
                # ft.IconButton(
                #     tooltip="Try on deprecated website", 
                #     mouse_cursor=ft.MouseCursor.CLICK,
                #     icon=ft.Icons.LINK, 
                #     on_click=lambda _: self.page.launch_url("https://plambe.wuaze.com")
                # ),
                # ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, on_click=self._toggle_dark_mode),
            ],
        )

    # def toggle_dark_mode(self, e):
    #     if self.page.theme_mode == "light":
    #         self.page.theme_mode = "dark"
    #     else:
    #         self.page.theme_mode = "light"
    #     self.page.update()
    def get_info(self, e):
        info_banner = InfoBanner(self.page)
        info_banner.open_banner(page=self.page)
        self.page.update()
        
    def submit_bug(self, e):
        
        # self.page.launch_url("https://github.com/Plambe/RadioDropDown/issues/new")
        bug_report = SubmitBug(self.page)
        self.page.open(bug_report)
        # bug_report.open_dialog(page=self.page)
        self.page.update()
        
        


