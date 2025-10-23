import flet as ft


class InfoBanner(ft.Banner):
    def __init__(self, page): 
        pass
        super().__init__(
            bgcolor=ft.Colors.AMBER_100,
            leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
            content=ft.Text(
                value="Oops, there were some errors while trying to delete the file. What would you like to do?",
                color=ft.Colors.BLACK,
            ),
            actions = ft.TextButton(text="Cancel", on_click=lambda _: page.go("/"))
            # actions=[
            #     ft.TextButton(
            #         text="Retry", style=action_button_style, on_click=close_banner
            #     ),
            #     ft.TextButton(
            #         text="Ignore", style=action_button_style, on_click=close_banner
            #     ),
            #     ft.TextButton(
            #         text="Cancel", style=action_button_style, on_click=close_banner
            #     ),
            # ],
        
        )