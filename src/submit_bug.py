import flet as ft
from global_model import GlobalModel



class SubmitBug(ft.AlertDialog):
    def __init__(self, page):
        self.page = page
        super().__init__(
            modal=True,
            title=ft.Text("Please enter your comments", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.TextField(
                    label="Message", 
                    multiline=True,
                    min_lines=3
                ),
            ], 
            height=200, 
            width=300
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(e)),
                ft.ElevatedButton("Submit", on_click=self.submit_dialog),
            ],
         
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
    def open_dialog(e):
        print("Open")
        # page.dialog = dialog
        # dialog.open = True
        # page.update()

    # def close_dialog(self,e):
    #     print("Close")
    #     self.page.close(e)
    #     # page.dialog = None
    #     # dialog.open = False
    #     # page.update()

    def submit_dialog(e):
        print("Submit")
        # if name_field.value and email_field.value:
        #     result_text.value = f"Name: {name_field.value}\nEmail: {email_field.value}\nMessage: {message_field.value}"
        #     # Clear fields for next use
        #     name_field.value = ""
        #     email_field.value = ""
        #     message_field.value = ""
        #     close_dialog(e)
        # else:
        #     # Show error
        #     page.show_snack_bar(ft.SnackBar(content=ft.Text("Please fill name and email!")))
    
   