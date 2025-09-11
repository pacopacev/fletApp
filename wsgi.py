import os
import flet as ft
import flet_fastapi
from main import main

# Create FastAPI app with Flet
app = flet_fastapi.app(main)

# Optional: Add additional FastAPI routes if needed
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# For direct execution (useful for testing)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)