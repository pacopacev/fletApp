import os
import sys

# Add the src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

print("=== DEBUG INFO ===")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# List files for verification
print("Files in current directory:")
for file in os.listdir('.'):
    print(f"  {file}")

print("Files in src directory:")
for file in os.listdir('src'):
    print(f"  {file}")

# Now import directly from src (no src. prefix needed)
from main import main

if __name__ == "__main__":
    import flet as ft
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Flet app on port {port}")
    ft.app(target=main, port=port, view=ft.WEB_BROWSER)