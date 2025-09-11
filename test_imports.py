import os
import sys

# Same setup as wsgi.py
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')

sys.path.insert(0, current_dir)
sys.path.insert(0, src_dir)

print("Testing direct imports with path modification...")

try:
    from main import main
    print("✓ main import successful")
    
    from appbar import AppBar
    print("✓ appbar import successful")
    
    from bottom_appbar import BottomAppBar
    print("✓ bottom_appbar import successful")
    
    from drop_downs import DDComponents
    print("✓ drop_downs import successful")
    
    print("✓ All direct imports working correctly!")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()