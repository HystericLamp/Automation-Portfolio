import os
import subprocess
import sys

"""
    This Script helps to setup environment by automatically
    creating a virtual environment and installs dependencies:
    - Selenium
"""

# Define the virtual environment directory
venv_dir = ".venv"

# Check if .venv already exists
if os.path.exists(venv_dir):
    print(f"Virtual environment '{venv_dir}' already exists.")
else:
    # Else create virtual environment
    print("Creating virtual environment...")
    subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
    print(f"Virtual environment '{venv_dir}' created.")

# Activate the virtual environment
if os.name == "nt":  # Windows
    activate_script = os.path.join(venv_dir, "Scripts", "activate")
else:  # Unix or MacOS
    activate_script = os.path.join(venv_dir, "bin", "activate")

print(f"To activate the virtual environment, run: source {activate_script}" if os.name != "nt" else f"Run: {activate_script}")

# Install Beautifulsoup in the virtual environment
print("Installing Beautifulsoup...")
subprocess.check_call([os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip"), "install", "beautifulsoup4"])
print("Beautifulsoup installed successfully.")

# Install Requests in the virtual environment
print("Installing Requests...")
subprocess.check_call([os.path.join(venv_dir, "bin", "python") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "python"), "-m", "pip", "install", "requests"])
print("Requests installed successfully.")

# Install XlsxWriter in the virtual environment
print("Installing XlsxWriter...")
subprocess.check_call([os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip"), "install", "XlsxWriter"])
print("XlsxWriter installed successfully.")

# Install pandas in the virtual environment
print("Installing pandas...")
subprocess.check_call([os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip"), "install", "pandas"])
print("pandas installed successfully.")

# Install python-docx in the virtual environment
print("Installing python-docx...")
subprocess.check_call([os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip"), "install", "python-docx"])
print("python-docx installed successfully.")

# Install openpyxl in the virtual environment
print("Installing openpyxl...")
subprocess.check_call([os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip"), "install", "openpyxl"])
print("openpyxl installed successfully.")