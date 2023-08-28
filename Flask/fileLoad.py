# Import the necessary Python libraries
from flask import request
from werkzeug.utils import secure_filename
import SQL_Functions as sq
import webLoadFunctions as wb

def loadFromFile(inputFile):
    
    #Initialize Variables
    source = "FILE"
    
    # Get the file from the request
    file = inputFile

    # Save the file to a temporary location
    filename = secure_filename(file.filename)
  
#   file.save(os.path.join(app.config['C:\\PythonProjects\\LLM\\Flask\\temp'], filename))

    # Load the contents of the file into a string
    file_content = file.read().decode('utf-8')

    # Add enty in history table for this file
    curLoadTimeStamp = wb.addLoadHistoryInDB(source)

    # Load content in database
    wb.loadDataInDB (source, filename, file_content)
    