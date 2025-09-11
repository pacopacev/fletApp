import os
from src.main import main
import flet as ft

# Create app using Flet's built-in FastAPI integration
app = ft.app(main, port=int(os.environ.get("PORT", 8000)), view=None)

# For direct execution
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)