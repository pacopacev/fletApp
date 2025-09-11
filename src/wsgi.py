import flet as ft
import flet_fastapi
from main import main

# Create FastAPI app with Flet
app = flet_fastapi.app(main)

# Optional: Add additional FastAPI routes if needed
@app.get("/health")
async def health_check():
    return {"status": "healthy"}