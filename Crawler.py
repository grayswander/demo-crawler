import logging
import queue
import threading
import time

from CrawlerQueue import CrawlerQueue
from CrawlerResultProcessor import CrawlerResultProcessor


class Crawler:
    def __init__(self, url: str, concurrency: int = 2, throttle: int = 3, max_depth: int = 3, max_docs: int = 100, output: str = './data' ):
        self.url = url
        self.concurrency = concurrency
        self.throttle = throttle
        self.max_depth = max_depth
        self.max_docs = max_docs
        self.output = output

    def run(self):
        """Crawl through a provided URL and store the results in a directory."""

        qm = self.create_queue()

        qm.add(self.url, 0)

        for i in range(self.concurrency):
            thread = threading.Thread(target=self.worker_thread, args=(f'thread-{i}', qm))
            thread.start()

        logging.info('Waiting for threads to finish')
        for thread in threading.enumerate():
            if thread != threading.current_thread():
                thread.join()

        print(f'Processed {qm.docs} documents')
        for url in qm.processed_urls():
            print(url)

    def create_queue(self):
        qm = CrawlerQueue(self.max_depth, self.max_docs)
        return qm

    def worker_thread(self, worker_id: str, task_queue: CrawlerQueue):
        """Worker thread that executes the crawler tasks."""
        crawler_result_processor = CrawlerResultProcessor(worker_id, self.output)

        while True:
            try:
                task = task_queue.get()
                task.execute(crawler_result_processor.handle_crawler_result)
                # Sleep for throttle seconds
                time.sleep(self.throttle)
            except queue.Empty:
                logging.info(f'Thread: {worker_id} exiting')
                break
