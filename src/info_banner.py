import flet as ft
from info_txt import info_txt


class InfoBanner(ft.Banner):
    def __init__(self, page):
        super().__init__(
            bgcolor=ft.Colors.BLACK,
            leading=ft.Icon(ft.Icons.INFO, color=ft.Colors.WHITE, size=40),
            content=ft.Text(
                value=info_txt,
                color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD,
            ),
            actions=[
                ft.FilledButton(
                    text="Dissmiss", style=ft.ButtonStyle(color=ft.Colors.BLACK), bgcolor=ft.Colors.WHITE, on_click=self.close_banner
                ),
            ]
        )
    @staticmethod
    def open_banner(page):
        # print("OPENING INFO BANNER")
        info_banner = InfoBanner(page)
        info_banner.open = True
        page.add(info_banner)
        page.update()
        
    def close_banner(e, banner):
        # print(e)
        # print("CLOSING INFO BANNER")
        page = banner.page
        banner.open = False
        page.close(e)
        page.update()
  

    


        
    
          