#!/usr/bin/python
import argparse
import requests

parser = argparse.ArgumentParser(description='Fetch spanish news articles from UN News.')
parser.add_argument('start', type=int)
parser.add_argument('end', type=int)
args = parser.parse_args()

def fetch_stories(start, end):

    log = open('log' + str(start).zfill(5) + "-" + str(end).zfill(5) + '.txt', 'w')

    for x in range(start, end):
        
        url = 'http://www.un.org/spanish/News/story.asp?NewsID=' + str(x)
        r = requests.get(url, allow_redirects=False)
        print(url + ", " + str(r.status_code))
        log.write(url + ", " + str(r.status_code) + "\n")

        if (r.status_code == 200):
            article = open('raw_html/' + str(x).zfill(5) + '.html', 'wb')
            article.write(r.content)
            article.close()
        
        if (x%10 == 0):
            log.flush()

    log.close()

fetch_stories(args.start, args.end)