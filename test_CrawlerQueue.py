import unittest
from CrawlerQueue import CrawlerQueue
from CrawlerTask import CrawlerTask


class TestCrawlerQueue(unittest.TestCase):
    def setUp(self):
        self.crawler_queue = CrawlerQueue(max_depth=3, max_docs=100)

    def test_add_valid_url(self):
        url = "http://example.com"
        depth = 1
        self.assertTrue(self.crawler_queue.add(url, depth))
        self.assertEqual(self.crawler_queue.size(), 1)
        self.assertEqual(self.crawler_queue.docs, 1)

    def test_add_duplicate_url(self):
        url = "http://example.com"
        depth = 1
        self.assertTrue(self.crawler_queue.add(url, depth))
        self.assertTrue(self.crawler_queue.add(url, depth))
        self.assertEqual(self.crawler_queue.size(), 1)
        self.assertEqual(self.crawler_queue.docs, 1)

    def test_add_max_depth(self):
        url = "http://example.com"
        depth = 3
        self.assertFalse(self.crawler_queue.add(url, depth))
        self.assertEqual(self.crawler_queue.size(), 0)
        self.assertEqual(self.crawler_queue.docs, 0)

    def test_add_max_docs(self):
        url = "http://example.com"
        for i in range(100):
            self.assertTrue(self.crawler_queue.add(f"{url}/{i}", 1))
        self.assertEqual(self.crawler_queue.size(), 100)
        self.assertFalse(self.crawler_queue.add(f"{url}/101", 1))
        self.assertEqual(self.crawler_queue.docs, 100)

    def test_get(self):
        url = "http://example.com"
        depth = 1
        self.crawler_queue.add(url, depth)
        task = self.crawler_queue.get()
        self.assertIsInstance(task, CrawlerTask)
        self.assertEqual(task.url, url)

    def test_empty(self):
        self.assertTrue(self.crawler_queue.empty())
        self.crawler_queue.add("http://example.com", 1)
        self.assertFalse(self.crawler_queue.empty())

    def test_size(self):
        self.assertEqual(self.crawler_queue.size(), 0)
        self.crawler_queue.add("http://example.com", 1)
        self.assertEqual(self.crawler_queue.size(), 1)

    def test_processed_urls(self):
        self.assertEqual(self.crawler_queue.processed_urls(), set())
        url = "http://example.com"
        self.crawler_queue.add(url, 1)
        self.assertEqual(self.crawler_queue.processed_urls(), {url})

if __name__ == '__main__':
    unittest.main()
