import os
import subprocess
import sys

"""
    This Script helps to setup environment by automatically
    creating a virtual environment and installs dependencies:
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

#####################################################################
# Unit Test Dependencies
#####################################################################
# Install Pytest in the virtual environment
print("Installing Unit Test Dependencies...")
print("Installing pytest...")
subprocess.check_call([os.path.join(venv_dir, "bin", "pip") if os.name != "nt" 
                       else os.path.join(venv_dir, "Scripts", "pip"), "install", "pytest"])
print("pytest installed successfully.")

######################################################################
# Email Access Dependencies
######################################################################
print("Installing Email Access Dependencies...")
print("Installing imapclient...")
subprocess.check_call([os.path.join(venv_dir, "bin", "pip") if os.name != "nt" 
                       else os.path.join(venv_dir, "Scripts", "pip"), "install", "imapclient"])
print("imapclient installed successfully.")

######################################################################
# Gmail API Dependencies
######################################################################
print("Installing Gmail API Dependencies...")
print("Installing google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client...")
subprocess.check_call([os.path.join(venv_dir, "bin", "pip") if os.name != "nt" 
                       else os.path.join(venv_dir, "Scripts", "pip"), "install", "google-auth",
                                                                                 "google-auth-oauthlib",
                                                                                 "google-auth-httplib2",
                                                                                 "google-api-python-client"])
print("google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client installed successfully.")