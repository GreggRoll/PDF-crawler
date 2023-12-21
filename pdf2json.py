import pdfplumber
import json
import glob

def pdf_to_json(pdf_path):
    """Uses pdfplumber package to format pdfs as a json as {filename, content} returns a json_object
    
    Keyword arguments:
    pdf_path -- path to .pdf file to be jsonified
    """
    text_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text from each page
            text = page.extract_text()
            if text:
                text_content.append(text)

    # Example of structuring
    json_object = {
        "filename": pdf_path,
        "content": text_content
    }

    return json_object

def walk_pdfs_and_convert(pdf_list):
    """takes in a list of pdf files and saves them in json format to output.json
    
    Keyword arguments:
    pdf_list -- list of pdf paths ex. ["pdfs/pdf1.pdf"]
    """
    json_list = []
    for pdf in pdf_list:
        json_data = pdf_to_json(pdf)
        json_list.append(json_data)

    #save the JSON data to a file
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(json_list, f, indent=4)

# pdf_list = glob.glob("pdfs/*")

# walk_pdfs_and_convert(pdf_list)