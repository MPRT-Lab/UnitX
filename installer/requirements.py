import tkinter as tk
from tkinter import ttk
import subprocess
import threading
from tkinter import messagebox
import win32api as win
import platform

# Global variables to control the progress update simulation
installation_running = False
progress_value = 0

global system_os = platform.system()

def log_output(text):
    """Append text to the log text widget and auto-scroll."""
    log_text.insert(tk.END, text)
    log_text.see(tk.END)

def update_progress():
    """Simulate a determinate progress update while installation is running."""
    global progress_value, installation_running
    if installation_running:
        # Increase progress gradually (simulate progress), but cap at 95%
        if progress_value < 95:
            progress_value += 2  # You can adjust the increment value and timing
            progress_bar['value'] = progress_value
        # Schedule the next update after 100 ms
        root.after(100, update_progress)
    else:
        # Installation finished, ensure progress is set to 100%
        progress_bar['value'] = 100

def installation_done():
    """Update the UI when the installation is completed."""
    status_label.config(text="Installation completed!", fg="green")
    install_button.config(state=tk.NORMAL)
    win.Beep(400,1000)
    win.Beep(600, 500)
    win.Beep(480,1000)

def install_requirements():
    """Run the pip installation command and log its output in real time."""
    global installation_running, progress_value
    installation_running = True
    progress_value = 0
    progress_bar['value'] = 0

    command = "python -m pip install --upgrade pip && pip install AppOpener google-generativeai setuptools pyinstaller pyshortcuts"
    # Start the installation process
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True
    )

    # Read output line by line and update the log widget
    for line in process.stdout:
        root.after(0, log_output, line)
    
    process.wait()  # Wait for the installation process to finish
    installation_running = False
    root.after(0, installation_done)

def start_installation():
    """Disable the install button and start both the installation and progress update."""
    install_button.config(state=tk.DISABLED)
    status_label.config(text="Installing...", fg="blue")
    # Start the installation in a separate thread
    threading.Thread(target=install_requirements, daemon=True).start()
    # Start updating the progress bar
    root.after(100, update_progress)

def go_to_next_page():
    # Clear current window
    root.destroy()
    try:
        if system_os == "Windows":
            subprocess.run(['python', 'location.py'], check=True)
        elif system_os == "Linux":
            subprocess.run(['python3', 'requirements.py'], check=True)
        else:
            subprocess.run(['python', 'requirements.py'], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"an error occurred: {e}")

def go_to_back_page():
    root.destroy()
    try:
        if system_os == "Windows":
            subprocess.run(['python', 'welcome.py'])
        elif system_os == "Linux":
            subprocess.run(['python3', 'requirements.py'])
        else:
            subprocess.run(['python', 'requirements.py'])
    except Exception as e:
        messagebox.showerror('Error',f'an error occurred: {e}')

# Set up the main window
root = tk.Tk()
root.title("Install Dependencies")
root.geometry("600x400")

# Explanation text for why these packages are needed
explanation = (
    "These packages are required to use the features of AppOpener and Google Generative AI. "
    "Please wait until the installation completes. The log below will display the progress."
)
explanation_label = tk.Label(root, text=explanation, wraplength=580, justify="center")
explanation_label.pack(pady=10)

# Create a determinate progress bar (set maximum to 100)
progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=10)
progress_bar['maximum'] = 100
progress_bar['value'] = 0

# Status label to display the current installation status
status_label = tk.Label(root, text="Waiting to start installation...", font=("Helvetica", 10))
status_label.pack(pady=10)

# Button to start the installation process
install_button = tk.Button(root, text="Start Installation", command=start_installation)
install_button.pack(pady=10)

# Create a frame to hold the log text widget and its scrollbar
log_frame = tk.Frame(root)
log_frame.pack(pady=10, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(log_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text = tk.Text(log_frame, wrap="word", yscrollcommand=scrollbar.set, height=10)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=log_text.yview)

back_button = tk.Button(root, text='back', command=go_to_back_page)
back_button.pack(side=tk.LEFT,ipadx=10)

next_button = tk.Button(root, text="Next", command=go_to_next_page)
next_button.pack(side=tk.RIGHT,ipadx=10)

img = tk.PhotoImage(file='UnitX.png')
root.iconphoto(False, img)

# Set the window icon (for both the window and Taskbar)
try:
    root.iconbitmap("UnitX.ico")  # Ensure "favicon.ico" is in the same directory as this script
except Exception as e:
    messagebox.showwarning("Icon Warning", f"Failed to load icon:\n{str(e)}")


root.mainloop()
