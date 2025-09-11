import os
import sys

# Get the current directory (where wsgi.py is located)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import your app - no need for src. prefix since we're already in src/
from main import main

# Create the Flet FastAPI app
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