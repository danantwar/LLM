import langchain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 1000,
    chunk_overlap  = 20,
    length_function = len,
    add_start_index = True,
)

def contentspiltter(filecontent):
    chunks = text_splitter.create_documents([filecontent]) 
    return chunks
"""
file_path = 'C:\\Users\\jagadish.patil\\myTestEnv\\tempFiles\\PLEASE_READ_ME.txt'
# Create a PyPDFLoader to load the PDF document
with open(file_path) as file:
    filecontent = file.read()
    chunks = contentspiltter(filecontent)
    conn = sq.getconnection()
    source="FILE"
    filename="xyz"
    for i, chunk in enumerate(chunks):
        content_parts = str(i)+ "/" + str(enumerate(chunks))
        content_metadata = chunk.page_content
        content = chunk.page_content
        data = (source, filename, content, content_metadata, content_parts)                
        #print(content)
        # Insert records in Database table            
        sq.create_records(conn, data)        
    conn.close()
"""