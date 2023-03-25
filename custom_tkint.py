import customtkinter as ctk
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showerror
from functions import *



# Browse and upload files
def browse_files(entry_type, raw_sample, raw_sample_diagram, **kwargs):


    # Browse for .xlsx and .xls files only
    filepath = filedialog.askopenfilename(filetypes=(("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")))

    if filepath and is_excel(filepath):
        if entry_type == "raw":
            raw_sample: str = filepath
            raw_sample_df = pd.read_excel(raw_sample)
            message, color, bool_result_raw = dimension_validation(raw_sample_df, 96, 16)
            raw_status_label.configure(text=message, fg_color=color)

            return raw_sample, raw_sample_df

        elif entry_type == "diagram":
            raw_sample_diagram: str = filepath
            raw_sample_diagram_df = pd.read_excel(raw_sample_diagram)
            message, color, bool_result_diagram = dimension_validation(raw_sample_diagram_df, 8, 13)
            diagram_status_label.configure(text=message, fg_color=color)

            return raw_sample, raw_sample_diagram_df


        # if bool_result_raw and bool_result_diagram:
        #     upload_button.configure(state="normal")
        # else:
        #     upload_button.configure(state="disabled")

    elif filepath:
        showerror("Invalid file type", "Please select Excel files (.xls or .xlsx) only.")

    return raw_sample, raw_sample_diagram




def download_file():

    # TODO add the download code
    # Download output file given name from choose prompt
    # Open the file

    pass

# Custom tkinter window initialization
window = ctk.CTk()
window.title("Custom Tkinter")
window.geometry("400x400")

# Main label widget
label = ctk.CTkLabel(window,
                     text="Preprocessing",
                     font=("Arial", 20, "bold"),
                     width=20,
                     corner_radius=10)
label.pack(padx=10, pady=15, side="top", anchor="center")


# Frame for the browse file buttons and their status labels
frame = ctk.CTkFrame(window, fg_color="transparent", bg_color="transparent")
frame.pack(pady=10, side="top", anchor="center")


# Diagram status labels (valid or not), hidden by default until file uploaded
diagram_status_label = ctk.CTkLabel(frame, text="", width=10, height=1)
diagram_status_label.grid(row=1, column=1, pady=10)

raw_status_label = ctk.CTkLabel(frame, text="", width=10, height=1)
raw_status_label.grid(row=1, column=0, pady=10)



# File upload browse buttons
raw_browse_button = ctk.CTkButton(frame,
                                  text="Upload raw sample file",
                                  command=lambda: browse_files("raw", "", "", bool_result_raw=False))

raw_browse_button.grid(row=0, column=0, padx=10)

diagram_browse_button = ctk.CTkButton(frame,
                                      text="Upload plate diagram",
                                      command=lambda: browse_files("diagram", "", "", bool_result_diagram=False))

diagram_browse_button.grid(row=0, column=1, padx=10)

# Download file button, default disabled
download_button = ctk.CTkButton(window,
                                text="Download",
                                command=download_file,
                                state="disabled")

download_button.pack(pady=(10, 20), side="bottom", anchor="center")

# File upload button, disabled by default until both files uploaded
upload_button = ctk.CTkButton(window,
                              text="Upload",
                              state="enabled",
                              command=upload_files)


upload_button.pack(side="bottom", anchor="center")

# Run the window
window.mainloop()
