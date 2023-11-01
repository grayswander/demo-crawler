import logging
import queue

from CrawlerTask import CrawlerTask


class CrawlerQueue:
    def __init__(self, max_depth: int = 3, max_docs: int = 100):
        self.q = queue.Queue()
        self.deduplicated = set()
        self.max_depth = max_depth
        self.max_docs = max_docs
        self.docs = 0

    def add(self, url: str, depth: int) -> bool:
        """Adds a URL to the queue. Returns True if caller should continue adding URLs, False otherwise."""
        if url in self.deduplicated:
            logging.debug(f'URL: {url} already processed, skipping')
            return True

        if depth >= self.max_depth:
            logging.debug(f'URL: {url} is too deep, skipping')
            return False

        if self.docs >= self.max_docs:
            logging.debug(f'URL: {url} is too many docs, skipping')
            return False

        self.docs += 1
        self.q.put(CrawlerTask(url, depth, self))
        self.deduplicated.add(url)
        logging.info(f'Added URL: {url} to queue')
        return True

    def get(self) -> CrawlerTask:
        """Returns next crawler task from the queue."""
        return self.q.get(block=True, timeout=5)

    def empty(self) -> bool:
        return self.q.empty()

    def size(self) -> int:
        return self.q.qsize()

    def docs(self) -> int:
        return self.docs

    def join(self):
        self.q.join()

    def processed_urls(self) -> set:
        return self.deduplicated

    def __str__(self):
        return f'Queue Size: {self.size()}'
