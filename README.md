# Dataset-Divider-Gtk


Dataset Divider is a python app that uses Gtk and allows you to divide csv data files and display the resulting graphs. Only csv files downloaded from https://fred.stlouisfed.org/ are supported.

Requirements before you run this program:
1) You must have matplotlib installed. You may run the following command to install it: "pip install matplotlib".
2) You must have a directory named "csv" in the same directory as the python files. The "csv" directory must contain .csv files downloaded from https://fred.stlouisfed.org/ as this program is only designed to analyze that data. CSV files will not be provided in this repository to avoid copyright infringement.

To run, execute this command: python3 UI.py

Select the first and second datasets, then click on the "Display Graph" button. The graph of the first dataset divided by the second dataset will be displayed.
