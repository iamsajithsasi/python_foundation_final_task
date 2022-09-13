import argparse
import logging

from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests

parser = argparse.ArgumentParser(description="Python RSS Reader")

my_parser = argparse.ArgumentParser(
    prog="rss_ready.py",
    usage="%(prog)s [options] path",
    description="List RSS",
)

parser.add_argument(
    "URL",
    metavar="source",
    type=str,
    default="https://news.yahoo.com/rss/",
    nargs="?",
    help="RSS URL",
)


# optional arguments
parser._optionals.title = "optional arguments"
parser.add_argument(
    "--version",
    action="version",
    version="%(prog)s Version 2.0",
    help="Print version info",
)
parser.add_argument("--json", help="Print result as JSON in stdout", action='store_true')
parser.add_argument(
    "--verbose",
    help="puts verbose status messages",
    action="store_true",
)
parser.add_argument(
    "--limit", type=int, default=None, help="Limit news topics if this parameter provided"
)

parsed_args = parser.parse_args()

# verbose
if parsed_args.verbose:
    logging.basicConfig(level=logging.DEBUG)
logging.debug("Only shown in debug mode")

# json
is_JSON = parsed_args.json

# setup
news_list = []

def extractData(elm, content, type="text"):
    if type == "text":
        try:
            return elm.find(content).text
        except:
            return "None"
    else:
        try:
            return elm.find(content).get("url")
        except:
            return None


def printFeeds(news):
    if parsed_args.limit:
        news_limited = news[: parsed_args.limit]
    else:
        news_limited = news
    
    for a in news_limited:
        title = extractData(a, "title")
        date = extractData(a, "pubDate")
        link = extractData(a, "link")
        image = extractData(a, "media:content", "url")
        source = extractData(a, "source")
        source_url = extractData(a, "source", "url")

        article = {
            "title": title,
            "date": parse(date),
            "link": link,
            "image": image,
            "source": source,
            "source_url": source_url,
        }
        news_list.append(article)

        if not is_JSON:
            print("Title: ", article["title"])
            print("Date: ", article["date"])
            print("Link: ", article["link"])
            print("Image: ", article["image"], end="\n\n")

    if is_JSON:
        print(news_list)

def getFeeds(URL):

    newsXml = requests.get(URL)
    newsFeeds = BeautifulSoup(newsXml.content, features="xml")
    headLine = newsFeeds.find("title").text
    news = newsFeeds.findAll("item")
    print("Feed: ", headLine, end="\n\n")

    if len(news) == 0:
        return "No news available"
    else:
        printFeeds(news)


getFeeds(parsed_args.URL)