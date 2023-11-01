import logging
import queue

from CrawlerTask import CrawlerTask


class CrawlerQueue:
    """A queue for crawler tasks. Handles deduplication, max depth and max docs."""
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
        """Returns next crawler task from the queue. Allows a timeout to allow other threads to add URLs. A delegation method."""
        return self.q.get(block=True, timeout=5)

    def empty(self) -> bool:
        """Returns True if the queue is empty, False otherwise. A delegation method."""
        return self.q.empty()

    def size(self) -> int:
        """Returns the size of the queue. A delegation method."""
        return self.q.qsize()

    def docs(self) -> int:
        """Returns the number of documents processed."""
        return self.docs

    def join(self):
        """Joins the queue. A delegation method."""
        self.q.join()

    def processed_urls(self) -> set:
        """Returns the set of processed URLs."""
        return self.deduplicated

    def __str__(self):
        return f'Queue Size: {self.size()}'
