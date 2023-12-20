#this isn't working

# importing required modules
import PyPDF2
import difflib
import re
import json
 
# Function to compare texts and return differences
def compare_texts(text1, text2):
    # Splitting the texts into lines
    text1_lines = text1.splitlines()
    text2_lines = text2.splitlines()

    # Using difflib to compare the lines
    diff = difflib.unified_diff(text1_lines, text2_lines, lineterm='', fromfile='version1.0.pdf', tofile='version1.1.pdf')

    return '\n'.join(list(diff))

def convert_bullet_points_to_list(text):
    # This regex pattern might need to be adjusted based on your specific PDFs
    pattern = r'\n\W\s*(.+)'
    items = re.findall(pattern, text)
    return items

def pdf_to_json(pdf_path):
    text = get_pdf_text(pdf_path)
    bullet_points = convert_bullet_points_to_list(text)
    json_data = json.dumps(bullet_points, indent=4)
    return json_data

def get_pdf_text(pdf_path):
    # creating a pdf file object
    pdfFileObj = open(pdf_path, 'rb')
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    pdf = """"""
    for i in pdfReader.pages:
        page = i.extract_text()
        pdf+=page
    pdfFileObj.close()
    return pdf
    


v1 = pdf_to_json("version1.0.pdf")
print(v1)