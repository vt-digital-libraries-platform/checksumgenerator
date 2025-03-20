# Description: This program will scan all the digital objects in a directory and provide a digital receipt of the checksum and file information
# Created by: Jennifer Goyne
# Created Date: 04/08/2024
# Working Date: 04/08/2024
# # Last Updated Date: 04/9/2024 
# Updated Date: 04/9/2024 - Updating the Algorium SHA1 because the program only works with MD5 and SHA1
# Updated Date: 04/09/2024 - Added a progress bar for larger collections 
#

import os
import hashlib
import csv
from datetime import datetime

def calculate_hashes(file_path):
    sha1 = hashlib.sha1()
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            sha1.update(chunk)
            md5.update(chunk)
    return sha1.hexdigest(), md5.hexdigest()

def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_extension = os.path.splitext(file_name)[1]
    created_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    return file_name, file_path, file_size, file_extension, created_date

# To change how the progress bar looks, you can modify the progress_bar function below change the fill='' to fill='*'
def progress_bar(iterable, prefix='', suffix='', length=50, fill='', print_end="\n", use_color=True):
    total = len(iterable)
    def show_progress_bar(i):
        progress = length * (i + 1) // total
        bar = fill * progress + '' * (length - progress)
        if use_color:
            print(f'{prefix} [\033[1;32m{bar}\033[0m] {i+1}/{total} {suffix}', end=print_end)
        else:
            print(f'{prefix} {bar} {i+1}/{total} {suffix}', end=print_end)
    return show_progress_bar

def main(root_folder, fill='#'):
    output_csv = os.path.join(root_folder, 'checksumsha1.csv')
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['CollectionItemName', 'CollectionRelativePath', 'SHA1', 'MD5', 'FileSize', 'FileExtension', 'CreatedDate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Get total number of files for progress bar to work and print out the progress bar
        total_files = sum(len(files) for _, _, files in os.walk(root_folder))
        progress_callback = progress_bar(range(total_files), prefix='Processing files', suffix='', length=50, fill=fill, use_color=False, print_end="\r\n")

        file_count = 0
        for root, dirs, files in os.walk(root_folder):
            for file in files:
                file_path = os.path.join(root, file)
                sha1_hash, md5_hash = calculate_hashes(file_path)
                filename, filepath, filesize, file_extension, created_date = get_file_info(file_path)
                writer.writerow({'Filename': filename, 'File Path': filepath, 'SHA1 Hash': sha1_hash, 'MD5 Hash': md5_hash,
                                 'File Size': filesize, 'File Extension': file_extension, 'Created Date': created_date})
                file_count += 1
                progress_callback(file_count)

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    # Use Tkinter to open file explorer for directory selection, this should be cross-platform. I have not used this before but it should work.
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Allow user to select a directory and store the selected path
    root_folder = filedialog.askdirectory(title="Select the folder path where you want your digital objects to undergo checksum calculation.")
    


    # If user cancels the selection, then exit the program and let the user know they need to select a folder
    if not root_folder:
        print("No folder selected. Exiting.")
        exit()

    fill = input("Enter the character to fill the progress bar (default is ''): ")
    main(root_folder, fill)
    print("Program is complete. Checksums and file information are stored in the folder you selected")
