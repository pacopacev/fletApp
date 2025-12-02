import flet as ft
import math
import time
import random
import threading

class Color:
    RED = ft.Colors.RED
    GREEN = ft.Colors.GREEN
    YELLOW = ft.Colors.YELLOW
    BLUE = ft.Colors.BLUE
    PURPLE = ft.Colors.PURPLE
    CYAN = ft.Colors.CYAN
    WHITE = ft.Colors.WHITE

def main(page: ft.Page):
    page.title = "Flet Equalizer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLACK
    
    # Control variables
    is_running = False
    animation_thread = None
    
    # Colors for bars
    colors = [Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.PURPLE]
    
    # Create equalizer display container
    equalizer_container = ft.Container(
        width=400,
        height=300,
        bgcolor=ft.Colors.BLACK,
        padding=20,
        border=ft.border.all(2, ft.Colors.WHITE),
        border_radius=10,
    )
    
    # Title
    title = ft.Text(
        "🎵 COLORFUL EQUALIZER 🎵",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE
    )
    
    # Control buttons
    start_button = ft.ElevatedButton(
        "Start Animation",
        icon=ft.Icons.PLAY_ARROW,
        on_click=lambda e: start_animation(),
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE
    )
    
    stop_button = ft.ElevatedButton(
        "Stop Animation",
        icon=ft.Icons.STOP,
        on_click=lambda e: stop_animation(),
        bgcolor=ft.Colors.RED,
        color=ft.Colors.WHITE,
        disabled=True
    )
    
    def update_equalizer_display(bar_heights):
        """Update the visual display of the equalizer"""
        bars_display = ft.Column(spacing=2)
        
        # Create bars from top to bottom
        for level in range(13, 0, -1):
            row = ft.Row(spacing=5)
            for i, bar_height in enumerate(bar_heights):
                color = colors[i % len(colors)]
                if bar_height >= level:
                    # Create a colored block
                    block = ft.Container(
                        width=30,
                        height=15,
                        bgcolor=color,
                        border_radius=ft.border_radius.all(3)
                    )
                else:
                    # Create empty space
                    block = ft.Container(
                        width=30,
                        height=15,
                        bgcolor=ft.Colors.BLACK,
                        border_radius=ft.border_radius.all(3)
                    )
                row.controls.append(block)
            bars_display.controls.append(row)
        
        equalizer_container.content = bars_display
        page.update()
    
    def equalizer_animation():
        """The main equalizer animation loop"""
        nonlocal is_running
        while is_running:
            bar_heights = []
            for i in range(10):  # 10 bars
                base_height = 2 + abs(math.sin(time.time() * 2 + i * 0.5)) * 10
                noise = random.uniform(-2, 2)
                height_val = int(base_height + noise)
                bar_heights.append(max(1, min(13, height_val)))
            
            # Update the display
            update_equalizer_display(bar_heights)
            time.sleep(0.15)
    
    def start_animation():
        """Start the equalizer animation"""
        nonlocal is_running, animation_thread
        if not is_running:
            is_running = True
            start_button.disabled = True
            stop_button.disabled = False
            page.update()
            
            animation_thread = threading.Thread(target=equalizer_animation, daemon=True)
            animation_thread.start()
    
    def stop_animation():
        """Stop the equalizer animation"""
        nonlocal is_running
        is_running = False
        start_button.disabled = False
        stop_button.disabled = True
        page.update()
    
    # Layout
    controls_row = ft.Row(
        controls=[start_button, stop_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    
    main_column = ft.Column(
        controls=[
            title,
            equalizer_container,
            controls_row,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )
    
    page.add(main_column)

if __name__ == "__main__":
    ft.app(target=main)