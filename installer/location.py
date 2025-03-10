import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import subprocess
import os

def browse_folder():
    """Open a dialog to select the destination folder."""
    destination = filedialog.askdirectory(title="Select Destination Folder")
    if destination:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, destination)

def copy_files():
    """Copy UnitX.py and favicon.ico to the selected destination folder."""
    destination = folder_entry.get().strip()
    if not destination:
        messagebox.showerror("Error", "Please select a destination folder.")
        return

    # Define the source files (assumed to be in the same directory as this script)
    source_files = [
        os.path.join(os.getcwd(), "UnitX.py"),
        os.path.join(os.getcwd(), "UnitX.ico"),
        os.path.join(os.getcwd(), "UnitX.png")
    ]

    # Check if source files exist
    missing_files = [file for file in source_files if not os.path.exists(file)]
    if missing_files:
        messagebox.showerror("Error", f"Source file(s) not found:\n{', '.join(missing_files)}")
        return

    try:
        # Copy each file to the destination folder
        for source_file in source_files:
            dest_file = os.path.join(destination, os.path.basename(source_file))
            shutil.copy(source_file, dest_file)
        
        messagebox.showinfo("Success", f"Files copied successfully to:\n{destination}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy files:\n{str(e)}")

def go_to_next_page():
    # Clear current window
    root.destroy()
    try:
        subprocess.run(['python', 'finish.py'], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def go_to_back_page():
    root.destroy()
    try:
        subprocess.run(['python', 'requirements.py'])
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

# Set up the main window
root = tk.Tk()
root.title("Specify File Location")
root.geometry("500x200")

# Label and entry for the destination folder
folder_label = tk.Label(root, text="Select Destination Folder for UnitX app:")
folder_label.pack(pady=10)

folder_entry = tk.Entry(root, width=50)
folder_entry.pack(pady=5)

# Button to browse for destination folder
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(pady=5)

# Button to copy the files
copy_button = tk.Button(root, text="Copy Files", command=copy_files)
copy_button.pack(pady=20)

back_button = tk.Button(root, text='Back', command=go_to_back_page)
back_button.pack(side=tk.LEFT, ipadx=10)

next_button = tk.Button(root, text="Next", command=go_to_next_page)
next_button.pack(side=tk.RIGHT, ipadx=10)

# Set the window icon
img = tk.PhotoImage(file='UnitX.png')
root.iconphoto(False, img)

# Set the window icon (for both the window and Taskbar)
try:
    root.iconbitmap("UnitX.ico")  # Ensure "favicon.ico" is in the same directory as this script
except Exception as e:
    messagebox.showwarning("Icon Warning", f"Failed to load icon:\n{str(e)}")

root.mainloop()
