import os
import sys

def main():
    increment_version()
def increment_version():
        # Add parent directory to path for imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)

    from src.version import version
    last_key = list(version)[-1]
    print(f"App Version: {version[last_key]}")

    print(type(version[last_key]))

    last_version = int(version[last_key])
    new_version = last_version + 100
    print(f"New Version: {new_version}")


    # Add a new element to the version dictionary
    new_key = 'version'  # Replace with your desired key
    new_value = str(new_version)  # Replace with your desired value
    version[new_key] = new_value

    # Write the updated version dictionary back to the version.py file
    import importlib.util
    spec = importlib.util.spec_from_file_location("version", "../version.py")
    version_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version_module)
    version_module.version = version

    # Save the updated version module
    with open("../version.py", "w") as file:
        file.write("version = " + str(version_module.version))

    print(version)
    
if __name__ == "__main__":
    main()
    





