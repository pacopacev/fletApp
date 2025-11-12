import flet as ft
 



class BottomAppBar(ft.BottomAppBar):
    def __init__(self, licence_text = None, on_scoll_to_top = None, page = None):
        state = False
        try:
            state = bool(page.platform == ft.PagePlatform.WINDOWS or page.platform == ft.PagePlatform.LINUX)
        except Exception as e:
            print("Database query failed:", e)
         
    

        self.on_scoll_to_top = on_scoll_to_top
        super().__init__(
            height=66,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Row(
                
                controls=[
                    # ft.IconButton(icon=ft.Icons.NEW_RELEASES, icon_color=ft.Colors.WHITE),
                    licence_text,
                    ft.Container(expand=state),
                    ft.Container(
                        content = ft.Image(
                        src=f"/icons/arrow_circle_up_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.png", 
                        width=50, 
                        height=50,
                        tooltip=ft.Tooltip("Go to top of page"),
                        
                    ),
                      width=60,
                      on_click=lambda e: self.on_scoll_to_top(e)
                    ), 
                 
                ]
            ),
        )