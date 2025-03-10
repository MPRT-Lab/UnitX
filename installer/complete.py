import os
import threading
from tkinter import *
from tkinter import messagebox
import pythoncom  # برای فراخوانی CoInitialize
from pyshortcuts import make_shortcut

def find_file(start_path, target_file):
    """Recursively search for a file in all directories."""
    excluded_dirs = ["$Recycle.Bin", "System Volume Information", "Windows"]
    for root, dirs, files in os.walk(start_path):
        # Exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def auto_find_and_create_shortcut():
    """Automatically search for UnitX.exe and favicon.ico on all drives and create a shortcut."""
    found_exe_path = None
    found_icon_path = None

    # Initialize COM library
    pythoncom.CoInitialize()

    try:
        # Get all available drives on Windows
        drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
        for drive in drives:
            # Search for UnitX.exe
            if not found_exe_path:
                found_exe_path = find_file(drive, "UnitX.exe")
            # Search for favicon.ico
            if not found_icon_path:
                found_icon_path = find_file(drive, "UnitX.ico")
            
            # Stop searching if both files are found
            if found_exe_path and found_icon_path:
                break

        if found_exe_path:
            print(f"Found UnitX.exe at: {found_exe_path}")
        else:
            print("UnitX.exe was not found on any drive.")
            messagebox.showerror("File Not Found", "UnitX.exe was not found on your system.")
            return

        if found_icon_path:
            print(f"Found UnitX.ico at: {found_icon_path}")
        else:
            print("favicon.ico was not found. Using default icon.")
            found_icon_path = None  # Use default icon if not found

        # Create a shortcut on the desktop
        try:
            make_shortcut(
                found_exe_path,
                name='UnitX',
                desktop=True,
                icon=found_icon_path  # Use the found icon or None for default
            )
            print(f"Shortcut created on the desktop for: {found_exe_path}")
            messagebox.showinfo("Success", "Shortcut created successfully on the desktop!")
        except Exception as e:
            print(f"Failed to create shortcut: {str(e)}")
            messagebox.showerror("Shortcut Error", f"Failed to create shortcut:\n{str(e)}")

    finally:
        # Uninitialize COM library
        pythoncom.CoUninitialize()

def start_auto_find():
    """Run the auto search and shortcut creation in a separate thread."""
    threading.Thread(target=auto_find_and_create_shortcut, daemon=True).start()

# Create the main window
tk = Tk()
tk.title('Finish Installation')
tk.geometry("400x200")

# Button to automatically find UnitX.exe and create a shortcut
check = IntVar()
checkbox = Checkbutton(
    tk,
    text='Create a Shortcut to Desktop',
    variable=check,
    onvalue=1,
    offvalue=0,
    command=start_auto_find
)
checkbox.pack()

# Create a finish button to close the window
btn = Button(tk, text='Finish', command=tk.destroy)
btn.pack(pady=10)

# Set the window icon (for both the window and Taskbar)
try:
    tk.iconbitmap("UnitX.ico")  # Ensure "favicon.ico" is in the same directory as this script
except Exception as e:
    messagebox.showwarning("Icon Warning", f"Failed to load icon:\n{str(e)}")

# Run the main loop
tk.mainloop()
