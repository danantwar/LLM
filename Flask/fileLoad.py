# Import the necessary Python libraries
from werkzeug.utils import secure_filename
import fileLoadFunctions as fl
import fileReadFunctions as frf
import os
import SQL_Functions as sq 

def loadFromFile(inputFile):
    
    #Initialize Variables
    source = "FILE"
    
    # Get the file from the request
    file = inputFile
   
    # Save the file to a temporary location
    filename = secure_filename(file.filename)
    print(filename)
    temp_folder = 'C:\\Users\\jagadish.patil\\myTestEnv\\tempFiles'
    file.save(os.path.join(temp_folder, filename))
    
      # Load the contents of the file into a string
    file_path = os.path.join(temp_folder, filename)
    file_content = frf.read_file_content(file_path)

    # Add enty in history table for this file
    fl.addLoadHistoryInDB(source)

    # Load content in database
    fl.loadDataInDB (source, filename, file_content)

def loadFileinBulk(file_name, file_Path):
    
    #Initialize Variables
    source = "FILE"
    
    file_content = frf.read_file_content(file_Path)

    # Add enty in history table for this file
    fl.addLoadHistoryInDB(source)
    file_content = file_content.replace('\r', '').replace('\n', '')
    #file_content = file_content.replace('\xa0', ' ')
    # Load content in database
    fl.loadDataInDB (source, file_name, file_content)