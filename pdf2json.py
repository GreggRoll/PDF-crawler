import pdfplumber
import json
import glob

def pdf_to_json(pdf_path):
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
    json_list = []
    for pdf in pdf_list:
        json_data = pdf_to_json(pdf)
        json_list.append(json_data)

    #save the JSON data to a file
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(json_list, f, indent=4)

pdf_list = glob.glob("pdfs/*")

walk_pdfs_and_convert(pdf_list)