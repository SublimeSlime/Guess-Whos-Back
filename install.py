#!/usr/bin/env python3

import os
import sys
import platform
from pathlib import Path

def get_theme_directories():
    """Get the theme directories for both Vencord and Vesktop based on the OS."""
    if platform.system() == "Windows":
        appdata = os.getenv("APPDATA")
        return [
            Path(appdata) / "Vencord" / "themes",
            Path(appdata) / "Vesktop" / "themes"
        ]
    else:
        home = Path.home()
        return [
            home / ".config" / "Vencord" / "themes",
            home / ".config" / "vesktop" / "themes"
        ]

def main():
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.absolute()
    theme_files = ["hide.css", "spoon.css"]
    
    # Get theme directories
    theme_dirs = get_theme_directories()
    
    # Check if source theme files exist
    for file in theme_files:
        if not (script_dir / file).exists():
            print(f"Error: Source theme file '{file}' not found in {script_dir}")
            sys.exit(1)
    
    # Create symbolic links for each theme directory
    for theme_dir in theme_dirs:
        if not theme_dir.exists():
            print(f"Warning: Theme directory not found at {theme_dir}")
            continue
            
        for file in theme_files:
            target = theme_dir / file
            source = script_dir / file
            
            try:
                if target.exists():
                    if target.is_symlink():
                        target.unlink()
                    else:
                        print(f"Warning: {target} exists and is not a symlink. Skipping.")
                        continue
                
                if platform.system() == "Windows":
                    # On Windows, we need to use os.symlink with absolute paths
                    os.symlink(str(source), str(target), target_is_directory=False)
                else:
                    # On Unix-like systems, we can use relative paths
                    relative_source = os.path.relpath(source, target.parent)
                    target.symlink_to(relative_source)
                
                print(f"Created symlink for {file} in {theme_dir}")
            except Exception as e:
                print(f"Error: Failed to create symbolic link for {file} in {theme_dir}")
                print(f"Error details: {str(e)}")
                sys.exit(1)
    
    print("Discord Theme installed successfully!")

if __name__ == "__main__":
    main() 