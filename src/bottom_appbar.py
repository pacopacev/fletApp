import flet as ft
 



class BottomAppBar(ft.BottomAppBar):
    def __init__(self, licence_text = None, on_scoll_to_top = None, page = None):
        # state = False
        # try:
        #     state = bool(page.platform == ft.PagePlatform.WINDOWS or page.platform == ft.PagePlatform.LINUX)
        # except Exception as e:
        #     print("Database query failed:", e)
        # Always create a spacer container; on Android it won't expand, on desktop it will
        expand_container = ft.Container(expand=False)
        try:
            if page and hasattr(page, 'platform'):
                print("Page platform detected:", page.platform)
                if page.platform == ft.PagePlatform.WINDOWS or page.platform == ft.PagePlatform.LINUX:
                    expand_container.expand = True
        except Exception as e:
            # Silently ignore, spacer will just not expand
            pass
         
    

        self.on_scoll_to_top = on_scoll_to_top
        
        # Build controls list, filtering out None values (important for Android compatibility)
        controls = [
            licence_text,
            expand_container,
            ft.Container(
                content=ft.Image(
                    src=f"/icons/arrow_circle_up_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.png",
                    width=50,
                    height=50,
                    tooltip=ft.Tooltip("Go to top of page"),
                ),
                width=60,
                on_click=lambda e: self.on_scoll_to_top(e),
            ),
        ]
        # Remove None values to avoid Flet errors on Android
        controls = [c for c in controls if c is not None]
        
        super().__init__(
            height=66,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Row(controls=controls),
        )