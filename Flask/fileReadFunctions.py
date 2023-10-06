import PyPDF2
import json
from docx import Document
import langchain
from langchain.document_loaders import PyPDFLoader

def read_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    
def read_pdf_with_langchain(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    text = ''
    for page in pages:
        text += page.page_content    
    return text

def read_docx(file_path):
    doc = Document(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

def read_txt(file_path):
    with open(file_path, 'r') as txt_file:
        return txt_file.read()

def read_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return json.dumps(data, indent=4)  # Pretty-print the JSON data

def read_file_content(file_path):
    if file_path.lower().endswith('.pdf'):
       # return read_pdf(file_path)
        return read_pdf_with_langchain(file_path)
    elif file_path.lower().endswith('.docx'):
        return read_docx(file_path)
    elif file_path.lower().endswith('.txt'):
        return read_txt(file_path)
    elif file_path.lower().endswith('.json'):
        return read_json(file_path)
    else:
        return "Unsupported file format"

# file_path = r'C:\Users\jagadish.patil\myTestEnv\Files\Information Access Control Policy v2.2.pdf'

# file_content = read_file_content(file_path)
# print("File Content:")
# print(file_content)
