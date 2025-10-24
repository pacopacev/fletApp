import flet as ft
from info_txt import info_txt
class InfoDialog(ft.AlertDialog):
    def __init__(self, page):
        super().__init__(
            bgcolor=ft.Colors.BLACK,
            title=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.INFO, color=ft.Colors.WHITE, size=40),
                    ft.Text("Information", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ]
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            value=info_txt,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Divider(color=ft.Colors.WHITE, height=2),
                        ft.Text(
                            value="To dismiss, click the button below",
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                ),
                height=400,  # Set a fixed height for the dialog content
                width=600,   # Set a fixed width
            ),
            actions=[
                ft.FilledButton(
                    text="Dismiss",
                    style=ft.ButtonStyle(color=ft.Colors.BLACK),
                    bgcolor=ft.Colors.WHITE,
                    on_click=self.close_dialog
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    @staticmethod
    def open_banner(page):
        # print("OPENING INFO BANNER")
        info_banner = InfoDialog(page)
        info_banner.open = True
        page.add(info_banner)
        page.update()
        
    def close_dialog(e, banner):
        # print(e)
        # print("CLOSING INFO BANNER")
        page = banner.page
        banner.open = False
        page.close(e)
        page.update()