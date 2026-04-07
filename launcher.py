import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import urllib.request
import os
import sys

TEMP = os.environ.get("TEMP", os.path.expanduser("~"))

FILES = {
    "PayloadHub.exe": "https://raw.githubusercontent.com/Gabe-P3/Payloads/main/PayloadHub.exe",
    "UWP.exe":        "https://raw.githubusercontent.com/Gabe-P3/Payloads/main/UWP.exe",
    "Flarial.dll":    "https://raw.githubusercontent.com/Gabe-P3/Payloads/main/Flarial.dll",
    "Bor.dll":        "https://raw.githubusercontent.com/Gabe-P3/Payloads/main/Bor.dll",
    "ForceCloseOreUI.dll": "https://raw.githubusercontent.com/Gabe-P3/Payloads/main/ForceCloseOreUI.dll",
}

BG       = "#1a1a1a"
SURFACE  = "#202020"
GREEN    = "#2fd673"
BLUE     = "#5865f2"
TEXT     = "#cccccc"
MUTED    = "#696969"
WHITE    = "#ffffff"


def download_file(name, url, force=False):
    path = os.path.join(TEMP, name)
    if force and os.path.exists(path):
        os.remove(path)
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)


def launch_hub():
    subprocess.Popen([os.path.join(TEMP, "PayloadHub.exe")])


def run_launch(btn_launch, btn_update, status_lbl):
    btn_launch.config(state="disabled")
    btn_update.config(state="disabled")
    status_lbl.config(text="Checking files...", fg=MUTED)
    try:
        for name, url in FILES.items():
            status_lbl.config(text=f"Checking {name}...")
            download_file(name, url, force=False)
        status_lbl.config(text="Launching...", fg=GREEN)
        launch_hub()
        root.after(800, root.destroy)
    except Exception as e:
        status_lbl.config(text=f"Error: {e}", fg="#ff5555")
        btn_launch.config(state="normal")
        btn_update.config(state="normal")


def run_update(btn_launch, btn_update, status_lbl):
    btn_launch.config(state="disabled")
    btn_update.config(state="disabled")
    status_lbl.config(text="Updating...", fg=MUTED)
    try:
        for name, url in FILES.items():
            status_lbl.config(text=f"Downloading {name}...")
            download_file(name, url, force=True)
        status_lbl.config(text="Launching...", fg=GREEN)
        launch_hub()
        root.after(800, root.destroy)
    except Exception as e:
        status_lbl.config(text=f"Error: {e}", fg="#ff5555")
        btn_launch.config(state="normal")
        btn_update.config(state="normal")


root = tk.Tk()
root.title("Payload Hub Loader")
root.geometry("340x170")
root.resizable(False, False)
root.configure(bg=BG)
root.eval("tk::PlaceWindow . center")

# Title
title = tk.Label(root, text="Payload Hub Loader", bg=BG, fg=WHITE,
                 font=("Segoe UI", 13, "bold"))
title.pack(pady=(18, 2))

sub = tk.Label(root, text="Choose how to launch", bg=BG, fg=MUTED,
               font=("Segoe UI", 9))
sub.pack()

# Button frame
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=14)

btn_launch = tk.Button(btn_frame, text="Launch Current Files",
                       bg=GREEN, fg=WHITE, activebackground="#27c060",
                       activeforeground=WHITE, relief="flat",
                       font=("Segoe UI", 9, "bold"),
                       width=18, height=2, cursor="hand2")
btn_launch.grid(row=0, column=0, padx=(0, 8))

btn_update = tk.Button(btn_frame, text="Update & Launch",
                       bg=BLUE, fg=WHITE, activebackground="#4752c4",
                       activeforeground=WHITE, relief="flat",
                       font=("Segoe UI", 9, "bold"),
                       width=16, height=2, cursor="hand2")
btn_update.grid(row=0, column=1)

# Status label
status_lbl = tk.Label(root, text="", bg=BG, fg=MUTED,
                      font=("Segoe UI", 8))
status_lbl.pack()

btn_launch.config(command=lambda: threading.Thread(
    target=run_launch, args=(btn_launch, btn_update, status_lbl), daemon=True).start())
btn_update.config(command=lambda: threading.Thread(
    target=run_update, args=(btn_launch, btn_update, status_lbl), daemon=True).start())

root.mainloop()
