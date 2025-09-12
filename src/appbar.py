import flet as ft

class AppBar(ft.AppBar):
    def __init__(self):
        super().__init__(

            leading=ft.Image(src="Weathered Chevron with Spikes and Chains.png"),
            leading_width=40,
            title=ft.Text("Radio DropDown", size=20, weight="bold"),
            center_title=True,
    
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.IconButton(tooltip="Try on depricated website", icon=ft.Icons.LINK, on_click=lambda _: self.page.launch_url("https://plambe.wuaze.com")),
                ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, on_click=self._toggle_dark_mode),
             
        ],
        )

    def _toggle_dark_mode(self, e):
        if self.page.theme_mode == "light":
            self.page.theme_mode = "dark"
        else:
            self.page.theme_mode = "light"
        self.page.update()