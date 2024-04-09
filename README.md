# Checksum Generation and File Information Retrieval
# Overview
This Python script is designed to generate checksums (SHA1 and MD5) for files within a specified directory. Additionally, it retrieves various file information such as filename, file path, file size, file extension, and creation date. The primary use case is to prepare files for ingestion into a Digital Library by ensuring data integrity through checksum verification.

# Requirements
  Python 3.x  
  Python modules included in this script are as follows: os, hashlib, csv, datetime, tkinter (standard library)
  
# Usage
- Clone or download the script checksum_generator.py.
- Ensure you have Python installed on your system.
- Open a terminal or command prompt.
- Navigate to the directory containing the checksum_generator.py script.
- Execute the script by running the command: python checksum_generator.py.
# Instructions
Upon execution of the program, the user will be prompted to select a folder containing the files for which you want to generate checksums.
Once the folder is selected, the program will also prompt you to select a fill symbol but you can click enter to bypass this in the program.(Default is empty character '')  Next the program will begin processing the files.
During this process a progress bar will be displayed to indicate the status of the operation. 
After the program has completed then the checksums and file information will be stored in a CSV file named checksumsha1.csv within the folder the user selected.
Once the program has completed you will receive a completion message.
