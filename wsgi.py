import os
import sys

# Add both current directory and src/ to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')

sys.path.insert(0, current_dir)  # For wsgi.py itself
sys.path.insert(0, src_dir)      # For direct imports like "from appbar import AppBar"

# Debug info
print("=== DEBUG INFO ===")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Now you can import directly (no src. prefix needed)
from main import main

# Create Flet app
import flet as ft
app = ft.fastapi.app(main)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Flet app is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)