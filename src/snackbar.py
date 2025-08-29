import flet as ft

class Snackbar(ft.SnackBar):
    def __init__(self, message, bgcolor, length):

        if length is None:
            content = ft.Text(f"{message}", size=20, weight="bold")
        else:
            content = ft.Text(f"{message} ({length})", size=20, weight="bold")
        super().__init__(
            
            content=content,
            open=False,
            bgcolor=bgcolor
        )
