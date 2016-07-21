#!/usr/bin/python
import argparse
from lxml import etree, html
import glob, os
    
def get_clean_html(file_name):

    original_html = open(file_name, encoding="utf-8")
    parser = html.HTMLParser(remove_comments=True)    
    tree = html.fromstring(original_html.read(), parser=parser)
    original_html.close()

    # tidy up the file
    for tag in tree.xpath("//script|//link|//noscript"):
        tag.getparent().remove(tag)  
    format_head(tree)
    remove_elements_by_class(tree, "add-this")
    remove_elements_by_class(tree, "old-share")

    # grab the article parts
    story_headline = tree.get_element_by_id('story-headline').text

    # the full story is sometimes hiding in a div with an id...
    try:
        story_body = format_story(tree.get_element_by_id('fullstory'))
    except: 
        # sometimes it's in a span?
        for span in tree.find_class('fullstory'):
            story_body = format_story(span)
        
    # blow away the body 
    clear_body(tree)

    # add the headline and body back 
    add_div(tree, 'headline', story_headline)
    add_div(tree, 'story', story_body)

    return html.tostring(tree, pretty_print=True, encoding="utf-8")


def format_head(tree):
    for head in tree.iter("head"):
        head.text = "\n\t"
        children = list(head)
        for child in children:
            if child != children[-1]:
                child.tail = "\n\t"
            elif child == children[-1]:
                child.tail = "\n"


def format_story(story_div):
    for br in story_div.findall('.//br'):
        if br.tail is not None:
            br.tail = str(br.tail) + "\n"
    story_body = story_div.text_content().strip().replace("  ", " ")
    return story_body


def remove_elements_by_class(tree, class_name):
    for element in tree.find_class(class_name):
        element.getparent().remove(element)


def clear_body(tree):
    for body in tree.iter("body"):
        body.clear()
        body.text = "\n"


def add_div(tree, id, text):
    div = html.fromstring("<div id ='" + id + "'>" + text + "</div>")
    tree.find('.//body').append(div)

parser = argparse.ArgumentParser(description='Reduce news articles from UN News to headline, story and header meta data')
parser.add_argument('source_dir', type=str,  help='source directory containing downloaded .html')
parser.add_argument('dest_dir', type=str, help='destination directory')
args = parser.parse_args()

os.chdir(args.source_dir)
for file in glob.glob("*.html"):
    print(file)

    cleaned_html = open('../' + args.dest_dir + "//" + file, 'wb')
    cleaned_html.write(get_clean_html(file))
    cleaned_html.close()