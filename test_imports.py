import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    from src.main import main
    print("✓ src.main import successful")
    
    # Test that the imports inside main.py work
    print("✓ Main function imports working")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()