import os
import json
import shutil
import platform
from datetime import datetime
import sys

def get_vscode_settings_path():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ.get('APPDATA', ''), 'Code', 'User', 'settings.json')
    elif system == "Darwin":
        return os.path.expanduser('~/Library/Application Support/Code/User/settings.json')
    else:
        return os.path.expanduser('~/.config/Code/User/settings.json')

def update_settings():
    path = get_vscode_settings_path()
    
    print("--- VS Code Global ESLint Setup ---")
    
    # Check if path is valid
    if not path or not os.path.exists(path):
        print(f"\n[ERROR] Could not find VS Code settings at:\n{path}")
        print("Please ensure VS Code is installed and has been opened at least once.")
        return
    
    print(f"\n[SUCCESS] Found VS Code settings file.")
    
    # Explanation & Confirmation
    print("\nI am going to make the following changes:")
    print("1. Modify 'settings.json' to enable ESLint validation for .ts and .tsx files.")
    print("2. Modify 'settings.json' to enable 'Working Directories', allowing ESLint to scan closed files in the background.")
    print(f"3. Create a backup of your current settings.")
    
    confirm = input("\nDo you want to proceed? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Setup aborted by user.")
        sys.exit(0)
    
    print("\nProcessing...")
    
    # Backup with error handling
    backup_path = path + ".backup_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        shutil.copy2(path, backup_path)
        print(f"Backup created at: {backup_path}")
    except Exception as e:
        print(f"\n[ERROR] Failed to create backup: {e}")
        return
    
    # Read settings
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Could not parse settings.json: {e}")
        print("Your settings file might contain comments (JSONC format).")
        print("Please remove comments or use a JSONC-compatible parser.")
        return
    except Exception as e:
        print(f"\n[ERROR] Failed to read settings: {e}")
        return
    
    # Config to apply
    eslint_config = {
        "eslint.validate": [
            "javascript",
            "javascriptreact",
            "typescript",
            "typescriptreact"
        ],
        "eslint.workingDirectories": [
            {
                "directory": ".",
                "changeProcessCWD": True
            }
        ]
    }
    
    updated = False
    for key, value in eslint_config.items():
        if key not in data or data[key] != value:
            data[key] = value
            updated = True
    
    if updated:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print("\n[SUCCESS] Global settings updated successfully!")
            print("Please restart VS Code for changes to take effect.")
        except Exception as e:
            print(f"\n[ERROR] Failed to write settings: {e}")
            print(f"Your original settings have been backed up to: {backup_path}")
            return
    else:
        print("\n[INFO] Settings were already correct. No changes made.")

if __name__ == "__main__":
    update_settings()
