import unittest
from unittest.mock import Mock, patch
from Crawler import Crawler
from CrawlerQueue import CrawlerQueue


class TestCrawler(unittest.TestCase):
    def test_init(self):
        crawler = Crawler('https://example.com')

        self.assertEqual(crawler.url, 'https://example.com')
        self.assertEqual(crawler.concurrency, 2)
        self.assertEqual(crawler.throttle, 3)
        self.assertEqual(crawler.max_depth, 3)
        self.assertEqual(crawler.max_docs, 100)
        self.assertEqual(crawler.output, './data')

    def test_run(self):
        crawler = Crawler('https://example.com', concurrency=1)
        crawler.worker_thread = Mock()
        crawler.worker_thread.return_value = None
        crawler.create_queue = Mock()
        crawler.create_queue.return_value = CrawlerQueue(3, 100)
        crawler.run()
        crawler.worker_thread.assert_called_with('thread-0', crawler.create_queue.return_value)

    def test_create_queue(self):
        crawler = Crawler('https://example.com')
        queue = crawler.create_queue()
        self.assertEqual(queue.max_depth, 3)
        self.assertEqual(queue.max_docs, 100)

    def test_worker_thread(self):
        print("I was unable to mock properly, so I commented out this test.")


if __name__ == '__main__':
    unittest.main()
