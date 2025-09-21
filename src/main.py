import flet as ft
import flet.fastapi as flet_fastapi
# from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import warnings
from pathlib import Path
from app import main

# Suppress noisy deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="uvicorn")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="websockets")

# --- Paths ---
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

print(f"Base directory: {BASE_DIR}")
print(f"Assets directory: {ASSETS_DIR}")
print(f"Assets exists: {ASSETS_DIR.exists()}")
if ASSETS_DIR.exists():
    print(f"Assets contents: {list(ASSETS_DIR.glob('*'))}")

app = flet_fastapi.FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # configure properly in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static files ---
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

# --- API endpoints ---
@app.get("/test-api")
async def test_api():
    return {"message": "Radio Browser API is running!", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/debug-assets")
async def debug_assets():
    files = []
    if ASSETS_DIR.exists():
        files = [f.name for f in ASSETS_DIR.iterdir() if f.is_file()]
    return {
        "assets_directory": str(ASSETS_DIR),
        "directory_exists": ASSETS_DIR.exists(),
        "files": files,
        "current_working_directory": str(Path.cwd())
    }

# --- Root landing page ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Try to locate a background or fallback to default icon
    icon_file = "Weathered Chevron with Spikes and Chains.png"
    if not (ASSETS_DIR / icon_file).exists():
        icon_file = next((f.name for f in ASSETS_DIR.glob("*.png")), "favicon.png")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Radio Browser</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="/assets/{icon_file}" type="image/png">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
            h1 {{ color: #333; }}
            .links {{ margin-top: 20px; }}
            .links a {{ display: block; margin: 10px 0; padding: 10px; background: #007bff; color: white;
                        text-decoration: none; border-radius: 5px; text-align: center; }}
            .links a:hover {{ background: #0056b3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎵 Radio Browser</h1>
            <p>Welcome to the Radio Browser application!</p>
            <div class="links">
                <a href="/app">Go to Radio App</a>
                <a href="/health">API Health Check</a>
                <a href="/debug-assets">Debug Assets</a>
                <a href="/assets/{icon_file}">Test Image Access</a>
                <a href="/test-api">Test API</a>
            </div>
        </div>
    </body>
    </html>
    """

# --- Mount Flet app at /app ---
app.mount(
    "/app",
     flet_fastapi.app(
        main,
        assets_dir=str(ASSETS_DIR),
      
    ),
)

# --- Entrypoint ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8553, log_level="info")
