import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os
import win32api as win

def log_output(text):
    """Append text to the log widget and auto-scroll."""
    log_text.insert(tk.END, text)
    log_text.see(tk.END)

def browse_folder():
    """Let the user choose the folder containing UnitX.py."""
    folder = filedialog.askdirectory(title="Select Folder Containing UnitX.py")
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

def auto_find_unitx():
    """Automatically search for UnitX.py on drive C, excluding specific folders."""
    log_text.delete(1.0, tk.END)
    log_output("Searching for UnitX.py on drive C: ...\n")
    
    # List of folders to exclude from the search
    excluded_folders = [
        "$Recycle.Bin",
        "System Volume Information",
        "Windows",
        "installer"
    ]
    
    found_path = None
    
    # Walk through drive C (this can be slow on large drives)
    for root_dir, dirs, files in os.walk("C:\\"):
        # Exclude specific directories from the search
        dirs[:] = [d for d in dirs if d not in excluded_folders]
        
        # Check if UnitX.py exists in the current directory
        if "UnitX.py" in files:
            found_path = root_dir
            break
    
    if found_path:
        log_output(f"Found UnitX.py in: {found_path}\n")
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, found_path)
    else:
        log_output("UnitX.py was not found on drive C.\n")

def start_auto_find():
    """Run the auto search in a separate thread."""
    threading.Thread(target=auto_find_unitx, daemon=True).start()

def run_pyinstaller():
    """Run PyInstaller on UnitX.py in the selected folder and update the progress bar with each log line."""
    folder = folder_entry.get().strip()
    if not folder:
        messagebox.showerror("Error", "Please select a folder containing UnitX.")
        return

    # Check if UnitX.py exists in the selected folder
    script_path = os.path.join(folder, "UnitX.py")
    if not os.path.exists(script_path):
        messagebox.showerror("Error", f"UnitX was not found in:\n{folder}")
        return

    build_button.config(state=tk.DISABLED)
    log_text.delete(1.0, tk.END)
    status_label.config(text="Building...", fg="blue")
    log_output(f"Running command in:\n{folder}\n\n")
    log_output("Executing: pyinstaller --noconsole UnitX.py\n")
    
    # Reset progress bar
    progress_bar['value'] = 0

    command = "pyinstaller --onefile --noconsole --icon=UnitX.ico UnitX.py"

    def run_command():
        progress = 0
        try:
            process = subprocess.Popen(
                command,
                cwd=folder,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True
            )
            # For each line of output, update the log and progress bar
            for line in process.stdout:
                root.after(0, log_output, line)
                progress += 1
                # Update the progress bar exactly with each output line (capped at 100)
                root.after(0, progress_bar.configure, {'value': min(progress, 100)})
            process.wait()
        except Exception as e:
            root.after(0, log_output, f"\nAn error occurred: {str(e)}\n")
        finally:
            root.after(0, finish_build)

    threading.Thread(target=run_command, daemon=True).start()

def finish_build():
    """Finalize UI updates after the build is complete."""
    progress_bar['value'] = 100
    status_label.config(text="Build completed!", fg="green")
    build_button.config(state=tk.NORMAL)
    log_output("\nBuild completed!\n")
    win.Beep(400,1000)
    win.Beep(600, 500)
    win.Beep(480,1000)


def go_clear_page():
    root.destroy()
    try:
        subprocess.run(['python','complete.py'])
    except Exception as e:
        messagebox.showerror('Error',f'an error occurred {e}')

# --------------------------
# GUI Setup
# --------------------------
root = tk.Tk()
root.title("Building UnitX")
root.geometry("650x600")

explanation = (
    "1. Please select the folder where UnitX is located using the Browse button,\n"
    "   or click 'Find Automatically' to search on drive C.\n"
    "3. The progress bar will update as output is received from PyInstaller, and detailed logs will be displayed.\n"
    "Note: The progress bar updates based on each line of output (and will reach 100% when done)."
)
explanation_label = tk.Label(root, text=explanation, wraplength=600, justify="left")
explanation_label.pack(pady=10)

# Folder selection frame
folder_frame = tk.Frame(root)
folder_frame.pack(pady=5, fill=tk.X, padx=10)

folder_label = tk.Label(folder_frame, text="Folder containing UnitX.py:")
folder_label.pack(side=tk.LEFT, padx=5)

folder_entry = tk.Entry(folder_frame, width=50)
folder_entry.pack(side=tk.LEFT, padx=5)

browse_button = tk.Button(folder_frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT, padx=5)

find_button = tk.Button(folder_frame, text="Find Automatically", command=start_auto_find)
find_button.pack(side=tk.LEFT, padx=5)

# Button to run PyInstaller
build_button = tk.Button(root, text="Run PyInstaller", command=run_pyinstaller)
build_button.pack(pady=10)

finish = tk.Button(root, text='finish', command=go_clear_page)
finish.pack(pady=10)

# Progress bar (determinate mode)
progress_bar = ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate")
progress_bar.pack(pady=10)
progress_bar['maximum'] = 100
progress_bar['value'] = 0

# Status label
status_label = tk.Label(root, text="Waiting to start build...", font=("Helvetica", 10))
status_label.pack(pady=5)

# Log text widget to display output
log_label = tk.Label(root, text="Log:")
log_label.pack(pady=5)
log_text = tk.Text(root, wrap="word", height=20)
log_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

img = tk.PhotoImage(file='UnitX.png')
root.iconphoto(False , img)

# Set the window icon (for both the window and Taskbar)
try:
    root.iconbitmap("UnitX.ico")  # Ensure "favicon.ico" is in the same directory as this script
except Exception as e:
    messagebox.showwarning("Icon Warning", f"Failed to load icon:\n{str(e)}")


root.mainloop()
