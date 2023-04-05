# qPCR RadBio Preprocessor

This Python project is a GUI application built with Custom Tkinter attributes that easy and flexible preprocessing and validation of of raw quantitative chain polymerase (qPCR) data straight from native BioRad software (CFX Maestro). Pandas is used as the primary tool for manipulation and and unit tests is used for for input and output validation.

## Key Features

- Rapid preprocessing with Pandas of raw qPCR data and integration with your experiment-specific plate diagram layout
- Rigorous validation for file input and results output
- Comprehensive, real-time log display with dynamic warnings and notifications within the app

## Getting Started

1. Clone the repository and move into the folder

```bash
git clone https://github.com/ivankoros/qPCR_preprocess_tkinter
cd qPCR_preprocess_tkinter
```
2. Install the required Python dependencies with pip
```python
pip install -r requirements.txt
```

3. Launch the main script
```python
python /main_app/main.py
```

## Usage
1. Export your qPCR data directly from CFX Maestro (making sure to set your run's specific threshold) as a .xlsx file
  - Without any modifications, it should be 96 x 16 
2. Draw up the schematic of your plate diagram in a separate .xlsx file

  - Using a standard 96-well plate, your diagram should be have 8 well rows as letters and 12 columns as numbers
  
  - If you're doing duplicates, write the sample name + dup as its duplicate

    - To do this easily in Excel or LibreCalc, use the following formula to add "dup" to an adjacent cell, replacing 'A1' with the cell you wish to target
    
      ```R
      =IF(ISBLANK(A1),"", A1&" Dup")
      ```
  - If you need to exclude a sample, add any text other than its name with it.
  
    - In the example below, samples 'X95 dup' and 'X50' were both re-done during the experiment. Samples 'X95 Dup*' and 'X50 (redo)' won't be used in processing, replaced with the properly formatted samples 'X50' in cell E10 and 'X95 Dup' in F10.
        
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

 - Tests will be ran against the dimensions and contents of your file to validate them and provide visual feedback
 
5. Click upload

  - Make note of the logs on the right hand side, pointing to possible statistical outliers needing your manual review
  
6. Click download to download your output as an .xlsx or .xls file. It will open after saving. 


## Animation
![](media/qPCR_tkinter_animation.gif)

## Contributing

Pull requests are enthusiastically welcome. For major changes, please open an issue first to discuss the proposed modifications.

## License

[MIT](https://choosealicense.com/licenses/mit/)


