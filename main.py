import logging

import typer

from Crawler import Crawler
from CrawlerQueue import CrawlerQueue


def main(
        url: str,
        concurrency: int = typer.Option(2, help='Number of threads to use'),
        throttle: int = typer.Option(3, help='Number of seconds to wait between requests'),
        max_depth: int = typer.Option(3, help='Maximum depth to crawl'),
        max_docs: int = typer.Option(100, help='Maximum number of documents to crawl'),
        loglevel: str = typer.Option('INFO', help='Log level'),
        output: str = typer.Option('./data', help='Output directory for results')
):
    """Crawl through a provided URL and store the results in a directory."""

    numeric_level = getattr(logging, loglevel.upper(), None)
    logging.basicConfig(level=numeric_level)

    crawler = Crawler(url, concurrency, throttle, max_depth, max_docs, output)
    crawler.run()


if __name__ == '__main__':
    typer.run(main)
