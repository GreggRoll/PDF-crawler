import requests
from bs4 import BeautifulSoup
import json
import os

def extract_links(url):
    """extract all pdf links for a given url and return a dict of the links
    
    Keyword arguments:
    url -- url to extract pdf links from)"""

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links that end with .pdf
    pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))

    # create a dictionary of the item name and link for each PDF
    links_dict = {link.text:link['href'] for link in pdf_links}

    with open('links_dict.json', 'w') as f:
        json.dump(links_dict, f, indent=1)

    return links_dict

def save_pdfs(url, links_dict, max_pdfs=10):
    """this function takes in links_dict and saves each pdf to pdfs folder
    
    Keyword arguments:
    url -- url to extract pdf links from
    links_dict -- json file of file names and paths
    max_pdfs -- (optional) helps limit saved pdfs for testing"""
    #add counter break for testing 10 files
    counter = 0
    for pdf in links_dict :
        if counter >= max_pdfs :
            break
        pdf_path = links_dict[pdf]
        full_pdf_path = url+pdf_path
        pdf_request = requests.get(full_pdf_path)

        with open(f'pdfs\\{pdf_path}', 'wb') as pdf_file:
            pdf_file.write(pdf_request.content)
        counter += 1

# url = "https://irp.fas.org/doddir/army/"
# links_dict = extract_links(url)
# save_pdfs(url, links_dict)