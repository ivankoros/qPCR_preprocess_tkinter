import customtkinter as ctk
import os
import pandas as pd
import tkinter as tk
import numpy as np
from tkinter import filedialog
from tkinter.messagebox import showerror

raw_sample = ""
raw_sample_diagram = ""


def is_excel(filename):
    return filename.lower().endswith(('.xls', '.xlsx'))


def browse_files(entry_type):
    global raw_sample, raw_sample_diagram
    filepath = filedialog.askopenfilename(filetypes=(("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")))
    if filepath and is_excel(filepath):
        if entry_type == "raw":
            raw_sample = filepath
            if "T1000" in filepath:
                raw_status_label.configure(text="✓ Looks good", fg_color="green")
            else:
                raw_status_label.configure(text="✗ Should be 83 x 19, is 32 x 15", fg_color="red")
        elif entry_type == "diagram":
            raw_sample_diagram = filepath
            if "T1000" in filepath:
                diagram_status_label.configure(text="✓ Looks good", fg_color="green")
            else:
                diagram_status_label.configure(text="✗ Should be 83 x 19, is 32 x 15", fg_color="red")
    elif filepath:
        showerror("Invalid file type", "Please select Excel files (.xls or .xlsx) only.")
        return

    if raw_sample and raw_sample_diagram:
        upload_button.configure(state="normal")
    else:
        upload_button.configure(state="disabled")


def upload_files():
    global raw_sample, raw_sample_diagram

    if not is_excel(raw_sample) or not is_excel(raw_sample_diagram):
        showerror("Invalid file type", "Please select Excel files (.xls or .xlsx) only.")
        return

    # Read data
    df_data = pd.read_excel(raw_sample, sheet_name=0)
    df_diagram = pd.read_excel(raw_sample_diagram)

    # TODO add preprocessing code here

    # Activate download button
    download_button.configure(state="normal")


def download_file():
        #TODO add the download code
    #Download output file given name from choose ptompt


    # Open the file
    #os.startfile("")


window = ctk.CTk()
window.title("Custom Tkinter")
window.geometry("400x400")

# Widgets
label = ctk.CTkLabel(window,
                     text="Preprocessing",
                     font=("Arial", 20, "bold"),
                     width=20,
                     corner_radius=10)
label.pack(padx=10, pady=15, side="top", anchor="center")

frame = ctk.CTkFrame(window, fg_color="transparent", bg_color="transparent")
frame.pack(pady=10, side="top", anchor="center")


# Diagram labels
diagram_status_label = ctk.CTkLabel(frame, text="", width=10, height=1)
diagram_status_label.grid(row=1, column=1, pady=10)

raw_status_label = ctk.CTkLabel(frame, text="", width=10, height=1)
raw_status_label.grid(row=1, column=0, pady=10)

# File upload browse buttons
raw_browse_button = ctk.CTkButton(frame,
                                  text="Upload raw sample file",
                                  command=lambda: browse_files("raw"))
raw_browse_button.grid(row=0, column=0, padx=10)

diagram_browse_button = ctk.CTkButton(frame,
                                      text="Upload plate diagram",
                                      command=lambda: browse_files("diagram"))
diagram_browse_button.grid(row=0, column=1, padx=10)

download_button = ctk.CTkButton(window,
                                text="Download",
                                command=download_file,
                                state="disabled")

download_button.pack(pady=10, side="bottom", anchor="center")

upload_button = ctk.CTkButton(window,
                              text="Upload",
                              state="disabled",
                              command=upload_files)
upload_button.pack(side="bottom", anchor="center")


window.mainloop()
