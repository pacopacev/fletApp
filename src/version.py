
# Auto-generated version info
import os

APP_VERSION = '0.0.2'
MAJOR = 0
MINOR = 0
PATCH = 2
BUILD_DATE = '2024-06-10T12:30:45Z'
COMMIT_HASH = 'a1b2c3d4'

# Version string in your desired format
version = f"V{os.getenv('APP_VERSION', APP_VERSION)} Build: {os.getenv('BUILD_DATE', BUILD_DATE)}"
print(f"Version loaded: {version}")