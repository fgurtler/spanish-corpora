#!/usr/bin/python
import argparse
import requests

parser = argparse.ArgumentParser(description='Fetch spanish news articles from UN News.')
parser.add_argument('start', type=int)
parser.add_argument('end', type=int)
args = parser.parse_args()

def fetch_stories(start, end):

    with open('log' + str(start).zfill(5) + "-" + str(end).zfill(5) + '.txt', 'w') as log:

        for x in range(start, end):
            
            url = 'http://www.un.org/spanish/News/story.asp?NewsID=' + str(x)
            r = requests.get(url, allow_redirects=False)
            print(url + ", " + str(r.status_code))
            log.write(url + ", " + str(r.status_code) + "\n")

            if (r.status_code == 200):
                with open('raw_html/' + str(x).zfill(5) + '.html', 'wb') as article:
                    article.write(r.content)
            
            if (x%10 == 0):
                log.flush()

fetch_stories(args.start, args.end)