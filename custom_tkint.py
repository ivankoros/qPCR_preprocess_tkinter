import customtkinter as ctk
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showerror
from functions import *
import os


# Browse and upload files
def browse_files(entry_type, raw_sample, raw_sample_diagram):

    filepath = filedialog.askopenfilename(filetypes=(("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")))

    if filepath and is_excel(filepath):
        if entry_type == "raw":
            raw_sample.set(filepath)
            raw_sample_df = pd.read_excel(raw_sample.get())
            message, color, bool_result_raw = dimension_validation(raw_sample_df, 96, 16)
            raw_status_label.configure(text=message, fg_color=color)

        elif entry_type == "diagram":
            raw_sample_diagram.set(filepath)
            raw_sample_diagram_df = pd.read_excel(raw_sample_diagram.get())
            message, color, bool_result_diagram = dimension_validation(raw_sample_diagram_df, 8, 13)
            diagram_status_label.configure(text=message, fg_color=color)

    elif filepath:
        showerror("Invalid file type", "Please select Excel files (.xls or .xlsx) only.")

def upload_files(raw_sample_df, raw_sample_diagram_df):

    global output_df

    if raw_sample_df is None or raw_sample_diagram_df is None:
        print(f"raw_sample_df: {raw_sample_df}, raw_sample_diagram_df: {raw_sample_diagram_df}")
        return
    output_df, st_dev_warnings = upload_files_preprocessing(raw_sample_df, raw_sample_diagram_df)

    download_button.configure(state="normal", text="Output file ready for download")

    print(st_dev_warnings)

    return output_df, st_dev_warnings


def download_file():
    if output_df is not None:
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel files", "*.xlsx")])
        if filename:
            output_df.to_excel(filename, index=False)
            os.startfile(filename)

            # Reset components to their default state
            raw_sample.set("")
            raw_sample_diagram.set("")
            raw_status_label.configure(text="", fg_color="transparent")
            diagram_status_label.configure(text="", fg_color="transparent")
            download_button.configure(state="disabled", text="Download")

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

raw_sample = tk.StringVar()
raw_sample_diagram = tk.StringVar()
raw_sample_df = None
raw_sample_diagram_df = None

# File upload browse buttons
raw_browse_button = ctk.CTkButton(frame,
                                  text="Upload raw sample file",
                                  command=lambda: browse_files("raw", raw_sample, raw_sample_diagram))

raw_browse_button.grid(row=0, column=0, padx=10)

diagram_browse_button = ctk.CTkButton(frame,
                                      text="Upload plate diagram",
                                      command=lambda: browse_files("diagram", raw_sample, raw_sample_diagram))

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
                              command=lambda: upload_files(pd.read_excel(raw_sample.get()), pd.read_excel(raw_sample_diagram.get())))


upload_button.pack(side="bottom", anchor="center")

# Run the window
window.mainloop()
