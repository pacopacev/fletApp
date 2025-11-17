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

        icon_data = ft.Icon(name=ft.Icons.ARROW_CIRCLE_UP, color=ft.Colors.WHITE, size=30)

        def handle_scroll_to_top(e):
            if self.on_scoll_to_top:
                self.on_scoll_to_top(e) 

        
        # Set floating action button if page is provided
        if page:
                page.floating_action_button = ft.FloatingActionButton(
                    icon=ft.Icons.ARROW_CIRCLE_UP,
                    icon_size=40,
                    icon_color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.LIME_300,
                    on_click=handle_scroll_to_top,
                    tooltip="Scroll to Top",
                    elevation=3
                )
        
        self.on_scoll_to_top = on_scoll_to_top
        
        super().__init__(
            height=54,
            bgcolor="#B00020",
            content=licence_text,
            padding=ft.padding.only(top=0, right=5, bottom=0, left=0),
            shape=ft.RoundedRectangleBorder(radius=15),
            notch_margin=5
        )