import os
import sys

# Add src to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# Import main
from main import main

if __name__ == "__main__":
    import flet as ft
    port = int(os.environ.get("PORT", 8000))
    ft.app(target=main, port=port, view=ft.WEB_BROWSER)