import flet as ft
import os 



class AppBar(ft.AppBar):
    def __init__(self):
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
                        on_click=self._toggle_dark_mode
                    ),
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

    def _toggle_dark_mode(self, e):
        print("Toggling dark mode...")
        print(f"Current theme mode: {self.page.theme_mode}")
        if self.page.theme_mode == "light":
            self.page.theme_mode = "dark"
        else:
            self.page.theme_mode = "light"
        self.page.update()


