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
from datetime import datetime
import os
import importlib.util


# project root (one level above src)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
version_path = os.path.join(parent_dir, "version.py")
# attempt to load version.py explicitly from repo root
version = {}
try:
    spec = importlib.util.spec_from_file_location("version", version_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    version = getattr(mod, "version", {})
except Exception as ex:
    print(f"Could not load version from {version_path}: {ex}")
    version = {}

# normalize into usable values
if isinstance(version, dict):
    _ver_num = version.get('version', '1.0.66')
    _ver_build = version.get('build_date', datetime.now().strftime("%Y-%m-%d"))
    _ver_commit = version.get('commit_hash', '')
else:
    # if version is a plain string or something else
    _ver_num = str(version)
    print(f"Version: {_ver_num}")
    _ver_build = ''
    _ver_commit = ''

# print(f"App Version: v{_ver_num} (Build: {_ver_build})")
env = Environment(loader=FileSystemLoader('templates'))


version = f"V{_ver_num} (Build: {_ver_build})"
# version = "1.0.1"

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8553, log_level="info")
