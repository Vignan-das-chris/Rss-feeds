import feedparser
from logging_config import logging


def parse_feeds(feed_urls):
    articles = []
    for feed_url in feed_urls:
        feed = feedparser.parse(feed_url)
        articles.extend(feed.entries)
    return articles

def parse_feed(feed_url):
    logging.info("Parsing feed: %s", feed_url)
    try:
        # ... parse feed data ...
    except ParsingError as e:
        logging.error("Parsing error: %s", e)
