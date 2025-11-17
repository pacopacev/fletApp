import flet as ft
from info_txt import info_txt
import markdown
class InfoDialog(ft.AlertDialog):
    def __init__(self, page):

        self.info_txt = markdown.markdown(info_txt)
        
        super().__init__(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            title=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.INFO, size=40),
                    ft.Text("Information", weight=ft.FontWeight.BOLD),
                ]
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Markdown(
                            value=info_txt,
                            selectable=True,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            
                 
                            
                        )
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                ),
                width=700,
                height=500,
                padding=20,
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