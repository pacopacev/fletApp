import flet as ft
import flet.fastapi as flet_fastapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import warnings
from pathlib import Path
from global_model import GlobalModel
from app import main
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


version = "0.1.1"

# Suppress noisy deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="uvicorn")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="websockets")

# --- Paths ---
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

# print(f"Base directory: {BASE_DIR}")
# print(f"Assets directory: {ASSETS_DIR}")
# print(f"Assets exists: {ASSETS_DIR.exists()}")
if ASSETS_DIR.exists():
    pass
    # print(f"Assets contents: {list(ASSETS_DIR.glob('*'))}")

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
@app.get("/test-db")
async def db_health_check():
    try:
        global_model = GlobalModel()
        # Test a simple query
        result = await global_model.execute_query_all("SELECT * FROM flet_radios LIMIT 100;")
        r_result = await global_model.execute_query_all("SELECT version() as db_version")
        return {"status": "healthy", "database": "connected", "db_version": r_result[0].get('db_version', 'unknown'),"radios_count_in_last_view": len(result)}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
# --- Root landing page ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Try to locate a background or fallback to default icon
    icon_file = "Weathered Chevron with Spikes and Chains.png"
    if not (ASSETS_DIR / icon_file).exists():
        icon_file = next((f.name for f in ASSETS_DIR.glob("*.png")), "favicon.png")

    return env.get_template('main_page_html.html').render(version=version, icon_file=icon_file)
       

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
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)
