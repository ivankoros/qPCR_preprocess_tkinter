import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
import pandas as pd
import re



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.upload1_button = tk.Button(self)
        self.upload1_button["text"] = "Upload raw data"
        self.upload1_button["command"] = self.upload_sample1_file
        self.upload1_button.pack()

        self.upload2_button = tk.Button(self)
        self.upload2_button["text"] = "Upload diagram"
        self.upload2_button["command"] = self.upload_sample2_file
        self.upload2_button.pack()

        self.submit_button = tk.Button(self)
        self.submit_button["text"] = "Submit"
        self.submit_button["command"] = self.run_script
        self.submit_button.pack()

        self.status_label = tk.Label(self)
        self.status_label.pack()

        self.download_button = tk.Button(self)
        self.download_button["text"] = "Download Output File"
        self.download_button["state"] = "disabled"
        self.download_button["command"] = self.download_output_file
        self.download_button.pack()

    def upload_sample1_file(self):
        filename = filedialog.askopenfilename()
        self.sample1_filename = filename
        if self.sample1_filename:
            self.upload1_button["text"] = self.sample1_filename

    def upload_sample2_file(self):
        filename = filedialog.askopenfilename()
        self.sample2_filename = filename
        if self.sample2_filename:
            self.upload2_button["text"] = self.sample2_filename


    def run_script(self):
        try:
            # Assign raw data and plate diagram files from user input
            RAW_SAMPLE_1 = self.sample1_filename
            RAW_SAMPLE_1_DIAGRAM = self.sample2_filename

            # Read in the raw data and plate diagram as pandas dataframes
            df_data = pd.read_excel(RAW_SAMPLE_1, sheet_name=0)
            df_diagram = pd.read_excel(RAW_SAMPLE_1_DIAGRAM)

            # Set the first column as the index, remove whitespace and add a space to the "dup" values
            df_diagram = df_diagram.set_index(df_diagram.columns[0])
            df_diagram = df_diagram.replace('\s+', '', regex=True)
            df_diagram = df_diagram.replace('dup', ' dup', regex=True)

            # Use the rows and columns (besides the first one) of the plate diagram to create a dictionary of
            # corresponding Sample and Well IDs
            sample_map = {}

            for row in df_diagram.index:
                for col in df_diagram.columns[1:]:
                    well_id = f"{row}{int(col):02d}"
                    sample_name = df_diagram.loc[row, col]
                    sample_map[well_id] = sample_name

            # Read in the raw qPCR data and map the well IDs to sample names using the dictionary
            df_data["Sample"] = df_data["Well"].map(sample_map)

            df = df_data[['Well', 'Cq', 'Sample']].copy()

            df['mtDNA1'] = "mtDNA1"
            df['mtDNA2'] = "mtDNA2"

            df = df.loc[:,["Well", "Sample", "mtDNA1", "mtDNA2", "Cq"]]

            df = df.dropna()

            # set mtDNA1 and mtDNA2 values to Cq values by treating mtDNA1 as the Cq for the first sample and mtDNA2
            # as the Cq for the duplicate sample if it exists as "Sample dup"

            for row, index in df.iterrows():
                df.loc[row, 'mtDNA1'] = df.loc[row, 'Cq']
                if df.loc[row, 'Sample'] + ' dup' in df['Sample'].values:
                    df.loc[row, 'mtDNA2'] = df.loc[df['Sample'] == df.loc[row, 'Sample'] + ' dup', 'Cq'].values[0]
                else:
                    df.loc[row, 'mtDNA2'] = np.NAN

            df = df.drop(columns=['Cq'])
            df = df.dropna()

            # Calculate standard deviation
            df['St.Dev'] = df[['mtDNA1', 'mtDNA2']].std(axis=1)

            for row, index in df.iterrows():
                if df.loc[row, 'St.Dev'] > .22:
                    print(
                        f"\n Warning: Standard deviation for {df.loc[row, 'Sample']} is {round(df.loc[row, 'St.Dev'], ndigits=3)} "
                        f"(Sample 1: {round(df.loc[row, 'mtDNA1'], ndigits=3)} vs Sample 2: {round(df.loc[row, 'mtDNA2'], ndigits=2)}) \n")

            df = df.sort_values(by=['St.Dev'], ascending=False)
            df = df.reset_index(drop=True)

            # Save output to file

            # Update UI
            self.status_label["text"] = "Done"
            self.df = df
            self.download_button["state"] = "normal"

        except Exception as e:
            self.status_label["text"] = f"Error: {str(e)}"
            self.df = None

    def download_output_file(self):
        try:
            if self.df is not None:
                filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
                if filename:
                    self.df.to_excel(filename, index=False)
                    self.status_label["text"] = "File saved"

                    # Clear files and reset buttons
                    self.sample1_filename = None
                    self.sample2_filename = None
                    self.df = None
                    self.upload1_button["text"] = "Upload raw data"
                    self.upload2_button["text"] = "Upload diagram"
                    self.download_button["state"] = "disabled"
                else:
                    self.status_label["text"] = "Download canceled"
            else:
                self.status_label["text"] = "Error: No data to download"
        except Exception as e:
            self.status_label["text"] = f"Error: {str(e)}"


root = tk.Tk()
root.geometry("400x150")
app = Application(master=root)
root.configure(bg="blue")
app.mainloop()