import os
import subprocess

"""
    This Script helps to setup environment
    by automatically installing required dependencies
"""
#####################################################################
# Unit Test Dependencies
#####################################################################
# Install Pytest in the virtual environment
print("Installing Unit Test Dependencies...")
print("Installing pytest...")
subprocess.check_call(["pip", "install", "pytest"])
print("pytest installed successfully.")

#####################################################################
# Python-dotenv
#####################################################################
print("Installing python-dotenv...")
subprocess.check_call(["pip", "install", "python-dotenv"])
print("python-dotenv installed successfully.")

######################################################################
# Gmail API Dependencies
######################################################################
print("Installing Gmail API Dependencies...")
print("Installing google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client...")
subprocess.check_call(["pip", "install", "google-auth",
                       "google-auth-oauthlib",
                       "google-auth-httplib2",
                       "google-api-python-client"])
print("google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client installed successfully.")