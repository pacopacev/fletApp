import os
import sys

# Add the src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

print("=== SERVER STARTUP ===")
print(f"Current directory: {os.getcwd()}")

from main import main

if __name__ == "__main__":
    import flet as ft
    port = int(os.environ.get("PORT", 8000))
    
    # assets_dir should be relative to main.py, which is in src/
    # So we point to the assets folder inside src/
    ft.app(
        target=main,
        port=port,
        view=ft.WEB_BROWSER,
        assets_dir="assets"  # Relative to main.py in src/
    )