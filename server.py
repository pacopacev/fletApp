import os
import sys

# Add the src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

print("=== DEBUG INFO ===")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Now import directly from src
from main import main

if __name__ == "__main__":
    import flet as ft
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Flet app on port {port}")
    
    assets_dir = None
    for possible_path in ['assets', 'src/assets']:
        if os.path.exists(possible_path):
            assets_dir = possible_path
            break
    
    print(f"Using assets directory: {assets_dir}")
    
    ft.app(
        target=main,
        port=port,
        view=ft.WEB_BROWSER,
        assets_dir=assets_dir,
        # Optional: Add more web settings
        web_renderer="canvaskit",
        use_color_emoji=True
    )