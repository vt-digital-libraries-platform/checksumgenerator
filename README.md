# Checksum Generation and File Information Retrieval
# Overview
The Python script is designed to generate checksums (SHA1 and MD5) for digital objects within a specified directory. Additionally, it retrieves various file information such as filename, file path, file size, file extension, and creation date. The primary use case is to prepare files for ingestion into a Digital Library by ensuring data integrity through checksum verification.  Also included in this repository is the checksum.go script for users that want to run this process in Go.

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
Upon running the program, the user will be prompted to choose a folder containing the digital objects for which checksum information is required. After selecting the folder, the program will offer the option to select a fill symbol; the user can skip this by pressing the enter key. Subsequently, the program will commence processing the files, displaying a progress bar to indicate the operation's status. Upon completion, the checksums and file information will be saved in a CSV file named checksumsha1.csv within the selected folder. Finally, a completion message will be displayed.
