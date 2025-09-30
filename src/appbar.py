import flet as ft


class AppBar(ft.AppBar):
    def __init__(self):

        super().__init__(
     
            leading=ft.Container(
                content=ft.Image(
                src=f"/Distressed Metal Chevron with Chains.png", 
                # width=30, 
                # height=30,
                tooltip=ft.Tooltip("Go to main page"),
                ), 
                 on_click=lambda _: self.page.launch_url("https://renewed-rosanne-pacopacev-b6447873.koyeb.app/"),
                 
                 
            ),
            toolbar_height=50,

            # leading=ft.Container(width=40, height=40),
            leading_width=50,
            title=ft.Row(
                controls=[
                    # ft.Image(src=f"/images/Weathered Chevron with Spikes and Chains.png", width=40, height=40), 
                    # ft.Text("Radio DropDown", size=20, weight="bold"), 
                    # ft.Image(src=f"images/Weathered Chevron with Spikes and Chains.png", width=40, height=40)
                ],
                alignment="center"
            ),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.IconButton(
                    tooltip="Try on deprecated website", 
                    mouse_cursor=ft.MouseCursor.CLICK,
                    icon=ft.Icons.LINK, 
                    on_click=lambda _: self.page.launch_url("https://plambe.wuaze.com")
                ),
                ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, on_click=self._toggle_dark_mode),
            ],
        )

    def _toggle_dark_mode(self, e):
        if self.page.theme_mode == "light":
            self.page.theme_mode = "dark"
        else:
            self.page.theme_mode = "light"
        self.page.update()