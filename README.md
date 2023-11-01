# Crawler

## Description
Crawles the provided URL and stores result in the output directory.

## Usage
```
Usage: main.py [OPTIONS] URL

  Crawl through a provided URL and store the results in a directory.

Arguments:
  URL  [required]

Options:
  --concurrency INTEGER  Number of threads to use  [default: 1]
  --throttle INTEGER     Number of seconds to wait between requests  [default:
                         3]
  --max-depth INTEGER    Maximum depth to crawl  [default: 3]
  --max-docs INTEGER     Maximum number of documents to crawl  [default: 100]
  --loglevel TEXT        Log level  [default: INFO]
  --output TEXT          Output directory for results  [default: ./data]
  --help                 Show this message and exit.
```

## Minimal example
```bash
python main.py https://foreternia.com/community/announcement-forum
```
This will crawl the provided URL and store the results in the `./data` directory.

## Docker
```bash
docker build -t crawler .
docker run -v `pwd`/data:/app/data -it --rm crawler --help
```

# Notes
- As mainly Java developer, I have little idea on proper Python project structure. Hence I have left it flat.
- I know that unit testing is important, but proper mocking requires a learning curve. I have added unit tests, which did not require complex mocking. Just to show that I know it should be done.
- I have tried to use `htmldate` package to determine publishing date, but was unable to install it on MacOS. Hence `CrawlerTask.CrawlerTask.deduce_date` relies on headers only.