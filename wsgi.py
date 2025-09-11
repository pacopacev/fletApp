import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the main function from your app
from main import main

# Create the Flet FastAPI app
import flet as ft
app = ft.fastapi.app(main)

# Add a health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Flet app is running"}

# For local testing
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)