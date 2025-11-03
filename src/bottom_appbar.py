import flet as ft
 



class BottomAppBar(ft.BottomAppBar):
    def __init__(self, licence_text = None):
        super().__init__(
            height=44,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            # shape=ft.NotchShape.CIRCULAR,
            content=ft.Row(
                
                controls=[
                    # ft.IconButton(icon=ft.Icons.NEW_RELEASES, icon_color=ft.Colors.WHITE),
                    licence_text,
                    # ft.Container(expand=True),
        
                 
                ]
            ),
        )