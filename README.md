# Custom Tkinter qPCR Preprocessor

This Python project is a GUI application built with Custom Tkinter attributes that easy and flexible preprocessing and validation of of raw quantitative chain polymerase (qPCR) data straight from native BioRad software (CFX Maestro). Pandas is used as the primary tool for manipulation and and unittests is used for for input and output validation.

## Key Features

- Seamless integration of raw sample data and plate diagram files in Excel format (.xls or .xlsx)
- Rigorous dimension validation employing algorithms that verify input files
- Robust data preprocessing utilizing advanced pandas DataFrame manipulation methods
- Generation of ready-to-download output files in Excel format
- Comprehensive, real-time log display with dynamic warnings and notifications within the app

## Usage
1. Export your qPCR data directly from CFX Maestro (making sure to set your run's specific threshhold) as a .xlsx file
  - Without any modifications, it should be 96 x 16 
2. Draw up the schematic of your plate diagram in a seperate .xlsx file

  - Using a standard 96-well plate, your diagram should be have 8 well rows as letters and 12 columns as numbers
  
  - If you're doing duplicates, write the sample name + dup as its duplicate
  
    - To do this easily in Excel or LibreCalc, use the following formula to add "dup" to an adjacent cell, replacing 'A1' with the cell you wish to target
    
      ```R
      =IF(ISBLANK(A1),"", A11&" Dup")
      ```
  - If you need to exclude a sample, add any text other than its name with it.
  
    - In the example below, samples 'X95 dup' and 'X50' were both re-done during the experiment. Samples 'X95 Dup*' and 'X50 (redo)' wont be used in processing, replaced with the properly formatted samples 'X50' in cell E10 and 'X95 Dup' in F10.
        
  |  	| 1 	| 2 	| 3 	| 4 	| 5 	| 6 	| 7 	| 8 	| 9 	| 10 	| 11 	| 12 	|
|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|
| A 	|  	| X123 	| X123 Dup 	| X124 	| X124 Dup 	| X125 	| X125 Dup 	| X126 	| X126 Dup 	| X127 	| X127 Dup 	|  	|
| B 	|  	| X45 	| X45 Dup 	| X59 	| X59 Dup 	| X48 	| X48 Dup 	| X86 	| X86 Dup 	| X88 	| X88 Dup 	|  	|
| C 	|  	| X44 	| X44 Dup 	| X40 	| X40 Dup 	| X53 	| X53 Dup 	| X82 	| X82 Dup 	| X106 	| X106 Dup 	|  	|
| D 	|  	| X106 	| X106 Dup 	| X98 	| X98 Dup 	| X46 	| X46 Dup 	| X104 	| X104 Dup 	| X61 	| X61 Dup 	|  	|
| E 	|  	| X95 	| **_X95 Dup\*_** 	| X102 	| X102 Dup 	| X76 	| X76 Dup 	| X114 	| X114 Dup 	| **X95 Dup** 	|  	|  	|
| F 	|  	| X42 	| X42 Dup 	| X88 	| X88 Dup 	| X58 	| X58 Dup 	| X69 	| X69 Dup 	| **X50** 	|  	|  	|
| G 	|  	| X76 	| X76 Dup 	| **_X50 (redo)_** 	| X50 Dup 	| X77 	| X77 Dup 	| X84 	| X84 Dup 	|  	|  	|  	|
| H 	|  	| X117 	| X117 Dup 	| X95 	| X95 Dup 	| X113 	| X113 Dup 	| X45 	| X45 Dup 	|  	|  	|  	|
 
 
3. Upload the plate diagram and the raw counts file into the application

 - Tests will be raun against the dimensions and contents of your file to validate them and provid visual feedback
 
5. Click upload

  - Make note of the logs on the right hand side, pointing to possible statisical outliers needing your manual review
  
6. Click download to donwload your output as an .xlsx or .xls file. It will open after saving. 


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

1. Export your qPCR data directly from CFX Maestro (making sure to set your experiment's threshhold) as a .xlsx file
2. Upload your plate diagram as follows:
4. Click "Upload raw sample file" to select and upload the raw sample data file in Excel format.
5. Click "Upload plate diagram" to select and upload the plate diagram file in Excel format.
6. Click "Upload" to initiate the state-of-the-art preprocessing algorithm, which processes the uploaded files and prepares the output file for download.
7. Click "Download" to save the expertly processed output file in Excel format.

## Contributing

Pull requests are enthusiastically welcome. For major changes, please open an issue first to discuss the proposed modifications.

## License

[MIT](https://choosealicense.com/licenses/mit/)

