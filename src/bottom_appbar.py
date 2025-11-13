import flet as ft
 
# from screeninfo import get_monitors

# # Get primary monitor
# monitor = get_monitors()[0]
# print(f"Screen width: {monitor.width}px")
# print(f"Screen height: {monitor.height}px")

# # Or get all monitors
# for i, monitor in enumerate(get_monitors()):
#     print(f"Monitor {i}: {monitor.width}x{monitor.height}")


class BottomAppBar(ft.BottomAppBar):
    def __init__(self, licence_text = None, on_scoll_to_top = None, page = None):
        # state = False
        # try:
        #     state = bool(page.platform == ft.PagePlatform.WINDOWS or page.platform == ft.PagePlatform.LINUX)
        # except Exception as e:
        #     print("Database query failed:", e)
        # Always create a spacer container; on Android it won't expand, on desktop it will
        # expand_container = ft.Container(expand=False, bgcolor = ft.Colors.RED)
        # try:
        #     if page and hasattr(page, 'platform'):
        #         print("Page platform detected:", page.platform)
        #         if page.platform == ft.PagePlatform.WINDOWS or page.platform == ft.PagePlatform.LINUX:
        #             expand_container.expand = True
        #         else:
        #             expand_container.content = ft.Text("Go to top")
        #             expand_container.expand = False
        # except Exception as e:
        #     # Silently ignore, spacer will just not expand
        #     pass
         
    

        self.on_scoll_to_top = on_scoll_to_top
        
        # Build controls list, filtering out None values (important for Android compatibility)
        controls = [
            licence_text,
            # expand_container,
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.ARROW_UPWARD,
                    icon_size=21,
                    tooltip=ft.Tooltip("Go to top of page"),
                    on_click=lambda e: self.on_scoll_to_top(e),
                    
                ),
                expand=True,
                alignment=ft.alignment.top_right,
            ),
        ]
        # Remove None values to avoid Flet errors on Android
        controls = [c for c in controls if c is not None]
        
        super().__init__(
            height=54,
            # bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            bgcolor=ft.Colors.BLACK,
            content=ft.Row(controls=controls),
            # shape=ft.NotchShape.CIRCULAR
            padding=ft.padding.only(top=10, bottom=0, left=5, right=10),
        )