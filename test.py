import flet as ft
import time
import threading

def main(page: ft.Page):
    page.title = "Moving Header Text Effect"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.colors.BLUE_GREY_900
    page.padding = 20

    # Create a container for the moving text
    text_container = ft.Container(
        width=page.width,
        height=80,
        bgcolor=ft.colors.TRANSPARENT,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # Create the moving text
    moving_text = ft.Text(
        value="WELCOME TO OUR WEBSITE • DISCOVER AMAZING THINGS • EXPLORE NOW • ",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.CYAN_ACCENT_400,
    )

    # Create a row to hold the text that will be animated
    text_row = ft.Row(
        controls=[moving_text],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Add the row to the container
    text_container.content = text_row

    # Function to animate the text
    def animate_text():
        position = 0
        while True:
            # Update the text position
            text_row.offset = ft.Offset(position, 0)
            page.update()
            
            # Move the text to the left
            position -= 0.5
            
            # Reset position when text moves completely off screen
            if position < -text_container.width:
                position = page.width
                
            time.sleep(0.02)

    # Start animation in a separate thread
    threading.Thread(target=animate_text, daemon=True).start()

    # Add some additional UI elements
    title = ft.Text(
        "Moving Header Effect",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.WHITE,
    )

    subtitle = ft.Text(
        "Smooth scrolling text animation",
        size=16,
        color=ft.colors.WHITE70,
    )

    # Add everything to the page
    page.add(
        title,
        subtitle,
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        text_container,
        ft.Divider(height=40, color=ft.colors.TRANSPARENT),
        ft.Text(
            "This text moves smoothly across the screen",
            size=18,
            color=ft.colors.WHITE60,
            italic=True
        )
    )

# Run the app
ft.app(target=main)