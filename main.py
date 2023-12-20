from crawler import extract_links, save_pdfs
from pdf2json import walk_pdfs_and_convert
from clustering import cluster
import glob
import json

#This script will extract all PDF links from the given url
url = "https://irp.fas.org/doddir/army/"
links_dict = extract_links(url)

#save the pdfs to pdfs folder
save_pdfs(url, links_dict)

#glob pdfs and convert to json outputting to output.json
pdf_list = glob.glob("pdfs/*")
walk_pdfs_and_convert(pdf_list)

#TODO! implement clustering.py to cluster files based on structure
with open("output.json") as f:
    json_objects = json.load(f)

cluster(json_objects)