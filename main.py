import customtkinter as ctk
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showerror
from functions import *
import os
import time


# Browse and upload files
def browse_files(entry_type, self):
    filepath = filedialog.askopenfilename(filetypes=(("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")))

    if filepath and is_excel(filepath):
        if entry_type == "raw":
            self.raw_sample = filepath
            self.raw_sample_df = pd.read_excel(self.raw_sample)
            message, color, bool_result_raw = dimension_validation(self.raw_sample_df, 96, 16)
            self.raw_status_label.configure(text=message, fg_color=color)

        elif entry_type == "diagram":
            self.raw_sample_diagram = filepath
            self.raw_sample_diagram_df = pd.read_excel(self.raw_sample_diagram)
            message, color, bool_result_diagram = dimension_validation(self.raw_sample_diagram_df, 8, 13)
            self.diagram_status_label.configure(text=message, fg_color=color)

    elif filepath:
        showerror("Invalid file type", "Please select Excel files (.xls or .xlsx) only.")


def upload_files(self):
    if self.raw_sample_df is None or self.raw_sample_diagram_df is None:
        timestamp = time.strftime("%H:%M @ %m/%d")
        update_log_text(self, "Error: Files not uploaded", "red")
        return
    output_df, st_dev_warnings = upload_files_preprocessing(self.raw_sample_df, self.raw_sample_diagram_df)

    self.download_button.configure(state="normal", text="Output file ready for download")

    print(st_dev_warnings)

    self.output_df = output_df
    self.st_dev_warnings = st_dev_warnings


def download_file(self):
    print(f"Download button clicked, output_df is: {self.output_df}")

    if self.output_df is not None:
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel files", "*.xlsx")])

        if filename:
            self.output_df.to_excel(filename, index=False)
            os.startfile(filename)

            # Reset components to their default state
            self.raw_sample = ""
            self.raw_sample_diagram = ""
            self.raw_status_label.configure(text="", fg_color="transparent")
            self.diagram_status_label.configure(text="", fg_color="transparent")
            self.download_button.configure(state="disabled", text="Download")


# Custom tkinter window initialization
class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Custom Tkinter")
        self.geometry("700x400")

        # Right-side log section
        self.log_section = ctk.CTkFrame(self,
                                        width=180,
                                        height=400)
        self.log_section.pack(side="right", fill="y", expand=False)

        # Log section title
        self.log_title = ctk.CTkLabel(self.log_section,
                                      text="Log",
                                      font=("Arial", 20, "bold"),
                                      width=250)
        self.log_title.pack(padx=10, pady=15, side="top")

        self.log_text = ctk.CTkTextbox(self.log_section,
                                       width=40,
                                       height=20,
                                       bg_color="transparent",
                                       font=("Arial", 10))
        self.log_text.pack(fill="both", expand=True, side="top", padx=10, pady=5)

        update_log_text(self, "Log started")

        # Main label widget
        self.label = ctk.CTkLabel(self,
                                  text="Preprocessing",
                                  font=("Arial", 20, "bold"),
                                  width=20,
                                  corner_radius=10)
        self.label.pack(padx=10, pady=15, side="top", anchor="center")

        # Frame for the browse file buttons and their status labels
        self.frame = ctk.CTkFrame(self, fg_color="transparent", bg_color="transparent")
        self.frame.pack(pady=10, side="top", anchor="center")

        # Diagram status labels (valid or not), hidden by default until file uploaded
        self.diagram_status_label = ctk.CTkLabel(self.frame, text="", width=10, height=1)
        self.diagram_status_label.grid(row=1, column=1, pady=10)

        self.raw_status_label = ctk.CTkLabel(self.frame, text="", width=10, height=1)
        self.raw_status_label.grid(row=1, column=0, pady=10)

        self.raw_sample = ""
        self.raw_sample_diagram = ""
        self.raw_sample_df = None
        self.raw_sample_diagram_df = None
        self.output_df = None
        self.st_dev_warnings = []
        self.output_df = None

        # File upload browse buttons
        self.raw_browse_button = ctk.CTkButton(self.frame,
                                               text="Upload raw sample file",
                                               command=lambda: browse_files("raw", self))

        self.raw_browse_button.grid(row=0, column=0, padx=10)

        self.diagram_browse_button = ctk.CTkButton(self.frame,
                                                   text="Upload plate diagram",
                                                   command=lambda: browse_files("diagram", self))

        self.diagram_browse_button.grid(row=0, column=1, padx=10)

        # Download file button, default disabled
        self.download_button = ctk.CTkButton(self,
                                             text="Download",
                                             command=lambda: download_file(self),
                                             state="disabled")

        self.download_button.pack(pady=(10, 20), side="bottom", anchor="center")

        # File upload button, disabled by default until both files uploaded
        self.upload_button = ctk.CTkButton(self,
                                           text="Upload",
                                           command=lambda: upload_files(self))

        self.upload_button.pack(pady=10, side="bottom", anchor="center")

        # Main loop
        self.mainloop()


if __name__ == "__main__":
    app = App()
