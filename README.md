# Custom Tkinter qPCR Preprocessor

This Python project is a GUI application built with Custom Tkinter attributes that allows rapid processing and validation of of quantitative chain polymerase data. The project uses custom tkinter and pandas libraries for data manipulation and visualization, and unittests for input and output validation.

## Key Features

- Seamless integration of raw sample data and plate diagram files in Excel format (.xls or .xlsx)
- Rigorous dimension validation employing algorithms that verify input files
- Robust data preprocessing utilizing advanced pandas DataFrame manipulation methods
- Generation of ready-to-download output files in Excel format
- Comprehensive, real-time log display with dynamic warnings and notifications within the app

## Animation
![](qPCR_tkinter_animation.gif)

## Getting Started

1. Clone the repository and move into the folder

```bash
git clone https://github.com/ivankoros/qPCR_preprocess_tkinter
cd qPCR_preprocess_tkinter
```
2. Install Python dependencies with pip
```python
pip install -r requirements.txt
```
3. Launch the main script
```python
python main.py
```
## Usage

1. Click "Upload raw sample file" to select and upload the raw sample data file in Excel format.
2. Click "Upload plate diagram" to select and upload the plate diagram file in Excel format.
3. Click "Upload" to initiate the state-of-the-art preprocessing algorithm, which processes the uploaded files and prepares the output file for download.
4. Click "Download" to save the expertly processed output file in Excel format.

## Contributing

Pull requests are enthusiastically welcome. For major changes, please open an issue first to discuss the proposed modifications.

## License

[MIT](https://choosealicense.com/licenses/mit/)

