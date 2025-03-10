import os
import socket
from tkinter import *
from tkinter import messagebox as msg
from tkinter.simpledialog import askstring
import google.generativeai as gen

# Function to check internet connection
def is_connected():
    try:
        # Try to connect to a well-known host (e.g., Google's DNS server)
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        return False

# Configure the Google Generative AI API
try:
    gen.configure(api_key='AIzaSyC3t7611QET4S8YWmhEN8Ndkqs63Kt1JHs')
    model = gen.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    msg.showerror("API Configuration Error", f"Failed to configure API: {str(e)}")
    exit()

# Initialize the main window
tk = Tk()
tk.title('UnitX App')
tk.geometry('500x500')

# List of forbidden directories to exclude from search
FORBIDDEN_DIRS = [
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
]

# Function to recursively search for a file
def find_file(start_path, target_file):
    for root, dirs, files in os.walk(start_path):
        # Exclude forbidden directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in FORBIDDEN_DIRS]
        
        if target_file in files:
            return os.path.join(root, target_file)
    return None

# Search for a file in all drives and directories
def search_all_drives(target_file):
    # Get all available drives on Windows
    drives = [f"{chr(drive_letter)}:\\" for drive_letter in range(65, 91) if os.path.exists(f"{chr(drive_letter)}:\\")]
    
    for drive in drives:
        try:
            result = find_file(drive, target_file)
            if result:
                return result
        except PermissionError:
            continue  # Skip directories with permission issues
    return None

# Find and load the image
image_path = search_all_drives('UnitX.png')
if image_path:
    try:
        img = PhotoImage(file=image_path)
        tk.iconphoto(False, img)
    except Exception as e:
        msg.showwarning("Icon Warning", f"Failed to load icon from '{image_path}':\n{str(e)}")
else:
    msg.showerror("File Error", "Image file 'UnitX.png' not found in any of the specified paths.")

# Find and load the favicon
favicon_path = search_all_drives('UnitX.ico')
if favicon_path:
    try:
        tk.iconbitmap(favicon_path)
    except Exception as e:
        msg.showwarning("Favicon Warning", f"Failed to load favicon from '{favicon_path}':\n{str(e)}")
else:
    msg.showerror("File Error", "Favicon file 'favicon.ico' not found in any of the specified paths.")

# Label for prompt
a = Label(tk, text="msg:")
a.place(x=10, y=10)

# Text widget with scrollbar
text_frame = Frame(tk)
text_frame.pack(padx=10, pady=10, expand=True, fill=BOTH)
scrollbar = Scrollbar(text_frame)
scrollbar.pack(side=RIGHT, fill=Y)
text_area = Text(text_frame, wrap=WORD, yscrollcommand=scrollbar.set, height=20, width=60)
text_area.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=text_area.yview)

# Function to handle user input and display responses
def show():
    b = askstring("What's your prompt?", "Please Input Message:")
    if b:
        # Check if there is an active internet connection
        if not is_connected():
            msg.showerror("Internet Error", "No Internet Connection")
            text_area.insert(END, "No Internet Connection\n")
            return
        
        try:
            if "pip" in b:
                result = os.system(f'{b}')
                text_area.insert(END, f"{result}\n")
                if '0' in str(result):
                    text_area.insert(END, "Successfully in Process PIP\n")
                if '1' in str(result):
                    text_area.insert(END, "Unsuccessfully in Process PIP.\n")
            elif 'open' in b:
                from AppOpener import open
                a = open(b.replace('open', ''))
                text_area.insert(END, f"{a}\n")
            else:
                # Send message to the Google Generative AI model
                chat = model.start_chat()
                response = chat.send_message(b)
                text_area.insert(END, f"- {response.text}\n")
        except Exception as e:
            # Check if the error has a status code (HTTP errors)
            if hasattr(e, 'status_code'):
                if e.status_code == 403:
                    msg.showerror("Access Denied", "Error 403: Access denied. Please check your API key or permissions.")
                elif e.status_code == 400:
                    msg.showerror("Bad Request", "Error 400: Bad request. Please check your input.")
                else:
                    msg.showerror("API Error", f"An API error occurred: {str(e)}")
            else:
                # Handle other unexpected errors
                msg.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
        
        # Auto-scroll to the end of the text area
        text_area.see(END)

def about():
    msg.showinfo("About UnitX","UnitX App and Unit of All Device system\nDesign and Created by MPRT Lab Team")

# Dark mode function
def darkmode():
    tk.configure(bg="black")
    a.config(background="black", fg="white")
    text_area.config(bg="black", fg="white")

# White mode function
def lightmode():
    tk.configure(bg='white')
    a.config(background="white", fg="black")
    text_area.config(bg="white", fg="black")

# Menu setup
menu = Menu(tk)
view = Menu(menu, tearoff=0)
menu.add_cascade(label='View', menu=view)
view.add_command(label='Light Mode', command=lightmode)
view.add_command(label='Dark Mode', command=darkmode)
help_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='About', command=about)
help_menu.add_separator()
help_menu.add_command(label='Exit', command=tk.destroy)

# Radio buttons for theme selection
v = IntVar(value=1)
e = Radiobutton(tk, text="white", variable=v, value=1, command=lightmode, border=2)
e.pack(anchor=E)
d = Radiobutton(tk, text="dark", variable=v, value=2, command=darkmode, border=2)
d.pack(anchor=E)

# Send button
b = Button(tk, text='Send a Message', command=show) 
b.pack(expand=True, anchor=S)

# Configure the menu
tk.config(menu=menu)

# Start the main loop
tk.mainloop()
