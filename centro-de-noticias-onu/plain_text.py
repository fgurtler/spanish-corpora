#!/usr/bin/python
import argparse
from lxml import html
import glob, os
    
def get_plain_text(file_name):
    with open(file_name, encoding="utf-8") as original_html:
	    tree = html.fromstring(original_html.read())
	    return tree.get_element_by_id('story').text

parser = argparse.ArgumentParser(description='Reduce news articles from UN News to plain text')
parser.add_argument('source_dir', type=str,  help='source directory containing cleaned .html')
parser.add_argument('dest_dir', type=str, help='destination directory')
args = parser.parse_args()

os.chdir(args.source_dir)
for file in glob.glob("*.html"):
    print(file)	
	
    base = os.path.basename(file)
    name = os.path.splitext(base)[0]

    with open('../' + args.dest_dir + "//" + name + ".txt", 'w', encoding='utf-8') as plain_text:
      plain_text.write(get_plain_text(file))
