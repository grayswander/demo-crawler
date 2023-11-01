import logging
import os
from dataclasses import dataclass, asdict
import json


@dataclass
class Result:
    """Represents the result of a crawler task."""
    url: str
    title: str
    published: str
    html: str


class CrawlerResultProcessor:
    """Processes the result of the crawler."""
    def __init__(self, thread_id: str, destination: str):
        self.thread_id = thread_id
        self.destination = destination

    def handle_crawler_result(self, url: str, depth: int, code: int, title: str, published: str, html: str):
        """Saves the result as JSON file."""

        logging.info(f'Thread: {self.thread_id} storing URL: {url}  Size: {len(html)} in {self.destination}')

        result = Result(url, title, published, html.decode('utf-8'))

        file_name  = f'{self.destination}/{self.thread_id}-{url.replace("/", "_").replace(":", "")}.json'
        logging.info(f'Thread: {self.thread_id} storing URL: {url} in {file_name}')

        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, 'w') as f:
            f.write(json.dumps(result.__dict__, indent=4))


