import os
import sys

# Add the current directory to Python path (so we can import src)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import from src package using absolute imports
from src.main import main

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