# ESLint Setup Scripts

Two Python scripts to automate ESLint configuration for React/TypeScript projects with VS Code.

## Prerequisites

Before running these scripts, ensure you have the following installed:

- **Python 3.x** - Required to run the setup scripts
- **Node.js and npm** - Required for installing ESLint dependencies
- **VS Code** - With the latest [ESLint extension](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) installed
- **A React/TypeScript project** - With a valid `package.json` file

> **Note:** The scripts automate ESLint configuration but do not install Python, Node.js, npm, or the VS Code ESLint extension. These must be installed manually beforehand.

---

## Scripts

### 1. `eslint_setup_helper.py`
Configures VS Code global settings for optimal ESLint integration.

**What it does:**
- Enables ESLint validation for `.ts` and `.tsx` files
- Configures ESLint working directories for background scanning
- Creates automatic backup of existing settings

> **Important:** This script only needs to be run **once**. It modifies your global VS Code user settings, which eliminates the need to create a `.vscode/settings.json` file in every single project.

**Usage:**
```bash
# Run from anywhere
python eslint_setup_helper.py
```

**Requirements:**
- VS Code installed and opened at least once

---

### 2. `eslint_new_project.py`
Configures ESLint for a new or existing React/TypeScript project.

**What it does:**
- Creates `eslint.config.js` with modern Flat Config format
- Installs required ESLint dependencies via npm
- Configures TypeScript, React Hooks, and React Refresh plugins

**Usage:**
```bash
# Navigate to your project root (where package.json is)
cd your-project-folder

# Run the script
python eslint_new_project.py
```

**Requirements:**
- Node.js and npm installed
- Valid `package.json` in current directory

---

## Quick Start

For a complete setup on a new React TypeScript project:

```bash
# 1. (One-time setup) Configure VS Code global settings
# Run this once to apply settings to all current and future projects
python eslint_setup_helper.py

# 2. (Per project) Set up the specific project
cd your-project-folder
python eslint_new_project.py

# 3. Restart VS Code and ESLint
# In VS Code: Ctrl+Shift+P → "ESLint: Restart ESLint Server"
```

---

## Dependencies Installed

The project setup script installs:
- `eslint`
- `globals`
- `typescript-eslint`
- `@eslint/js`
- `eslint-plugin-react-hooks`
- `eslint-plugin-react-refresh`

---

## Notes

- Both scripts create backups before making changes
- Both scripts require confirmation before proceeding
- Scripts are designed for React + TypeScript projects using Vite or similar setups

---

## License

MIT
