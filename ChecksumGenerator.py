# Description: This program scans all the digital objects in a directory and provides a digital receipt of the checksum and file information.
# Created by: Jennifer Goyne
# Created Date: 04/08/2024
# Last Updated Date: 04/23/2025
# Last Updated Date: 05/15/2025 - formatted the code and added comments
import os
import hashlib
import csv
from datetime import datetime

CHUNK_SIZE = 65536

def calculate_hashes(file_path):
    """Calculate SHA1 and MD5 hashes for a given file."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    sha1 = hashlib.sha1()
    md5 = hashlib.md5()
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            sha1.update(chunk)
            md5.update(chunk)
    
    return sha1.hexdigest(), md5.hexdigest()

def get_file_info(file_path):
    """Retrieve file metadata."""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_extension = os.path.splitext(file_name)[1]
    created_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    return file_name, file_path, file_size, file_extension, created_date

def progress_bar(iterable, prefix='', suffix='', length=50, fill='#', print_end="\n", use_color=True):
    """Display a progress bar."""
    total = len(iterable)
    
    def show_progress_bar(i):
        progress = length * (i + 1) // total
        bar = fill * progress + ' ' * (length - progress)
        if use_color:
            print(f'{prefix} [\033[1;32m{bar}\033[0m] {i+1}/{total} {suffix}', end=print_end)
        else:
            print(f'{prefix} [{bar}] {i+1}/{total} {suffix}', end=print_end)
    
    return show_progress_bar

def iter_files(root_folder):
    """Iterate over all files in a directory."""
    for root, _, files in os.walk(root_folder):
        for file in files:
            yield os.path.join(root, file)

def main(root_folder, fill='#'):
    """Main function to calculate checksums and write to a CSV file."""
    output_csv = os.path.join(root_folder, 'checksumsha1.csv')
    files = list(iter_files(root_folder))
    total_files = len(files)
    progress_callback = progress_bar(range(total_files), prefix='Processing files', length=50, fill=fill, use_color=False, print_end="\r\n")

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Filename', 'FilePath', 'SHA1_Hash', 'MD5_Hash', 'FileSize', 'FileExtension', 'CreatedDate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, file_path in enumerate(files):
            try:
                sha1_hash, md5_hash = calculate_hashes(file_path)
                filename, filepath, filesize, file_extension, created_date = get_file_info(file_path)
                writer.writerow({
                    'Filename': filename,
                    'FilePath': filepath,
                    'SHA1_Hash': sha1_hash,
                    'MD5_Hash': md5_hash,
                    'FileSize': filesize,
                    'FileExtension': file_extension,
                    'CreatedDate': created_date
                })
                progress_callback(i)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    # Use Tkinter to open file explorer for directory selection
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    root_folder = filedialog.askdirectory(title="Select the folder path for checksum calculation.")
    if not root_folder:
        print("No folder selected. Exiting.")
        exit()

    fill = input("Enter the character to fill the progress bar (default is '#'): ") or '#'
    main(root_folder, fill)
    print("Program is complete. Checksums and file information are stored in the selected folder.")

