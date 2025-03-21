import http.client
import subprocess
import tkinter as tk
from tkinter import messagebox
import importlib
import urllib.request as down
import sys
import requests
import os
import platform
import subprocess

global system_os = platform.system()

def download_latest_python():
    # URL of the official Python website to get the latest version info
    url = "https://www.python.org/ftp/python/"
    
    # Fetch the HTML content of the directory listing
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch Python versions.")
        return
    
    # Extract the latest version number from the directory listing
    versions = []
    for line in response.text.splitlines():
        if 'href="3.' in line:  # Assuming we are looking for Python 3.x
            version = line.split('href="')[1].split('/')[0]
            versions.append(version)
    
    if not versions:
        print("No Python versions found.")
        return
    
    latest_version = max(versions)
    print(f"Latest Python version: {latest_version}")
    
    # Determine the system architecture and OS
    system_os = platform.system()
    machine = platform.machine()
    
    if system_os == "Windows":
        python_url = f"{url}{latest_version}/python-{latest_version}-amd64.exe"
        installer_path = "python-latest-amd64.exe"
    elif system_os == "Linux":
        python_url = f"{url}{latest_version}/Python-{latest_version}.tgz"
        installer_path = f"Python-{latest_version}.tgz"
    elif system_os == "Darwin":  # macOS
        python_url = f"{url}{latest_version}/python-{latest_version}-macosx10.9.pkg"
        installer_path = "python-latest-macosx.pkg"
    else:
        print("Unsupported operating system.")
        return
    
    # Download the installer
    print(f"Downloading Python from: {python_url}")
    response = requests.get(python_url, stream=True)
    if response.status_code != 200:
        print("Failed to download Python installer.")
        return
    
    with open(installer_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    print(f"Python downloaded successfully: {installer_path}")
    
    # Run the installer (for Windows and macOS)
    if system_os in ["Windows", "Darwin"]:
        print("Running the installer...")
        subprocess.run([installer_path], check=True)
    elif system_os == "Linux":
        print("Extracting the tarball...")
        subprocess.run(["tar", "-xvzf", installer_path], check=True)
        print("Please follow the instructions to build and install Python manually.")

def check_python_installation():
    try:
        importlib.import_module('sys')
        label = tk.Label(root,text='Python is installed')
        label.pack(pady=5)
    except:
        download_latest_python()

def go_to_next_page():
    # Clear current window
    root.destroy()
    try:
        if system_os == "Windows":
            subprocess.run(['python', 'requirements.py'], check=True)
        elif system_os == "Linux":
            subprocess.run(['python3', 'requirements.py'], check=True)
        else:
            subprocess.run(['python', 'requirements.py'], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open the next script: {e}")

# Create the main window
root = tk.Tk()
root.title("Installer")
root.geometry("300x300")

# Initialize the first page
label = tk.Label(root, text="Welcome to the Installer", font=("Arial", 14))
label.pack(pady=20)

check_python_installation()

next_button = tk.Button(root, text="Next", command=go_to_next_page)
next_button.pack(ipadx=10,ipady=10,pady=10)

### Menu of installer 
def about():
    messagebox.showinfo(title='About Installer', message='Installer \n Created by MPRT Lab\n Version: 0.1')

menu = tk.Menu(root)

view = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='About', menu=view)
view.add_command(label='About', command=about)

root.config(menu=menu)
# Run the main loop

img = tk.PhotoImage(file='UnitX.png')
root.iconphoto(False, img)

# Set the window icon (for both the window and Taskbar)
try:
    root.iconbitmap("UnitX.ico")  # Ensure "favicon.ico" is in the same directory as this script
except Exception as e:
    messagebox.showwarning("Icon Warning", f"Failed to load icon:\n{str(e)}")

root.mainloop()
