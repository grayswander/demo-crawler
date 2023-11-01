import logging
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


class CrawlerTask:
    def __init__(self, url: str, depth: int, queue_ref):
        self.url = url
        self.depth = depth
        self.queue_ref = queue_ref

    def __str__(self):
        return f'URL: {self.url} Depth: {self.depth}'

    def find_links(self, soup: BeautifulSoup):
        """Finds links in the HTML and adds them to the queue."""

        for link in soup.find_all('a'):
            link_url = link.get('href')
            logging.debug(f"Found URL: {link_url}")
            link_url = self.normalize_url(link_url)
            logging.debug(f"Normalized URL: {link_url}")

            if "#" in link_url:
                logging.debug(f'Found anchor, skipping: {link_url}')
                continue

            if not self.queue_ref.add(link_url, self.depth + 1):
                logging.info(f'Queue is full, stopping further processing')
                break

    def normalize_url(self, link_url: str) -> str:
        """Normalizes the URL."""

        parsed_base = urlparse(self.url)

        host = "{parsed_base.scheme}://{parsed_base.netloc}".format(parsed_base=parsed_base)

        if link_url.startswith('http'):
            return link_url

        if link_url.startswith('//'):
            return f'http:{link_url}'

        if link_url.startswith('/'):
            return f'{host}{link_url}'

        return f'{self.url}/{link_url}'

    def execute(self, result_handler=None):
        """Executes the task."""
        logging.info(f'Processing URL: {self.url}')
        code, headers, html = self.retrieve_url()

        if code != 200:
            logging.info(f'URL: {self.url} returned HTTP code: {code}')
            return

        soup = BeautifulSoup(html, 'html5lib')

        title = soup.find('title')
        if title:
            title = title.text
        else:
            title = 'None'

        published_date = self.deduce_date(soup, headers)

        if published_date:
            published = published_date
        else:
            published = 'None'

        self.find_links(soup)

        if result_handler:
            result_handler(self.url, self.depth, code, title, published, html)

    def deduce_date(self, soup, headers: list):
        """Deduce the date of the article."""
        soup_find = soup.find('meta', {'name': 'published_date'})

        if soup_find:
            return soup_find.get('content')

        for header in headers:
            if header[0] == 'Date':
                return header[1]

        return None

    def retrieve_url(self) -> tuple[int, list, str]:
        """Retrieves the URL and returns the Response Code, List of Headers and HTML."""

        req = Request(
            self.url,
            headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            }
        )
        with urlopen(req) as response:
            code = response.getcode()

            if code != 200:
                return code, [], "None"

            response_headers = response.getheaders()

            html = response.read()
            return code, response_headers, html
