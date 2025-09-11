import os
import sys

# Add the current directory to Python path (so we can import src)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Print debug information
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# List files for debugging
print("Files in current directory:")
for file in os.listdir('.'):
    print(f"  {file}")

if os.path.exists('src'):
    print("Files in src directory:")
    for file in os.listdir('src'):
        print(f"  {file}")

# Import from src package
try:
    from src.main import main
    print("✓ Successfully imported from src.main")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    # Try alternative import approach
    try:
        import src.main as main_module
        main = main_module.main
        print("✓ Successfully imported using alternative approach")
    except ImportError as e2:
        print(f"✗ All import attempts failed: {e2}")
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