import os
import subprocess
import sys
import shutil

# Content for eslint.config.js
ESLINT_CONFIG_CONTENT = """import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  { ignores: ['dist'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
    },
  },
)
"""

def check_npm_available():
    """Check if npm is available in PATH"""
    npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
    return shutil.which(npm_cmd) is not None

def run_command(cmd, cwd):
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"\n[ERROR] Command not found: {cmd[0]}")
        print("Please ensure npm is installed and in your PATH.")
        return False

def create_eslint_config(path):
    """Create or overwrite ESLint config file"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(ESLINT_CONFIG_CONTENT.strip())
        return True
    except IOError as e:
        print(f"\n[ERROR] Failed to write file: {e}")
        return False

def setup_project():
    cwd = os.getcwd()
    package_json_path = os.path.join(cwd, 'package.json')
    eslint_config_path = os.path.join(cwd, 'eslint.config.js')

    print("--- Project ESLint Setup ---")

    # 1. Initial Validation
    if not os.path.exists(package_json_path):
        print("\n[ERROR] No 'package.json' found in this directory.")
        print("Please run this script from the root folder of your React/Node project.")
        sys.exit(1)

    if not check_npm_available():
        print("\n[ERROR] npm is not available in your PATH.")
        print("Please ensure Node.js and npm are installed.")
        sys.exit(1)

    print("\n[SUCCESS] Valid project detected (package.json found).")

    # 2. Explanation & Confirmation
    deps = "eslint, globals, typescript-eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh"
    print("\nI am going to perform the following actions:")
    print(f"1. Create/Overwrite 'eslint.config.js' with modern Flat Config settings.")
    print(f"2. Install dependencies via npm: {deps}")
    
    confirm = input("\nDo you want to proceed? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Setup aborted by user.")
        sys.exit(0)

    # 3. Execution
    print("\nProcessing...")

    # Handle config file creation
    config_created = False
    if os.path.exists(eslint_config_path):
        print(f"Warning: '{eslint_config_path}' already exists.")
        overwrite = input("Overwrite existing file? (y/n): ").strip().lower()
        if overwrite == 'y':
            if create_eslint_config(eslint_config_path):
                print(f"Updated: {eslint_config_path}")
                config_created = True
            else:
                print("Failed to update config file.")
        else:
            print("Keeping existing eslint.config.js file.")
            config_created = True  # Existing file is fine
    else:
        if create_eslint_config(eslint_config_path):
            print(f"Created: {eslint_config_path}")
            config_created = True
        else:
            print("Failed to create config file. Aborting.")
            sys.exit(1)

    # Install Dependencies
    dependencies = [
        "eslint",
        "globals",
        "typescript-eslint",
        "@eslint/js",
        "eslint-plugin-react-hooks",
        "eslint-plugin-react-refresh"
    ]
    
    print("\nInstalling dependencies...")
    npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
    cmd = [npm_cmd, "install", "-D"] + dependencies
    success = run_command(cmd, cwd)

    # Final status report
    print("\n-------------------------------------------------")
    if success and config_created:
        print("[SUCCESS] Project setup complete!")
        print("Next steps:")
        print("1. Open VS Code.")
        print("2. Press Ctrl+Shift+P -> 'ESLint: Restart ESLint Server'")
    elif success:
        print("[PARTIAL SUCCESS] Dependencies installed, but config file was not created.")
    else:
        print("[WARNING] Setup incomplete. Please check the errors above.")
    print("-------------------------------------------------")

if __name__ == "__main__":
    setup_project()
