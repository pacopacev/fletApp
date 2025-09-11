import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Debug information
print("=== DEBUG INFO ===")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

print("\nFiles in current directory:")
for file in os.listdir('.'):
    print(f"  {file}")

print("\nFiles in src directory:")
for file in os.listdir('src'):
    print(f"  {file}")

# Import main
try:
    from src.main import main
    print("✓ Successfully imported from src.main")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    
    # Try to debug by importing each module
    print("\nTrying to import individual modules:")
    try:
        import src.appbar
        print("✓ src.appbar imported successfully")
    except ImportError as e:
        print(f"✗ src.appbar import failed: {e}")
    
    try:
        import src.drop_downs
        print("✓ src.drop_downs imported successfully")
    except ImportError as e:
        print(f"✗ src.drop_downs import failed: {e}")
    
    try:
        import src.all_stations
        print("✓ src.all_stations imported successfully")
    except ImportError as e:
        print(f"✗ src.all_stations import failed: {e}")
    
    raise

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