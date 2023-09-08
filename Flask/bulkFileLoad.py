import os
import fileLoad as fl

# Define the directory path where your files are located
directory_path = 'C:\\Users\\jagadish.patil\\myTestEnv\\tempFiles'

# List all files in the directory
file_list = os.listdir(directory_path)

# Loop through each file and read its content
for filename in file_list:
    file_path = os.path.join(directory_path, filename)

    # Check if the file is a regular file (not a directory)
    if os.path.isfile(file_path):           
        fl.loadFileinBulk(filename, file_path)