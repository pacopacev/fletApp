import flet as ft
 



class BottomAppBar(ft.BottomAppBar):
    def __init__(self):
        super().__init__(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            shape=ft.NotchShape.CIRCULAR,
            content=ft.Row(
                controls=[
                    ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),
                    ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE),
                 
                ]
            ),
        )