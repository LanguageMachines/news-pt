import csv
import json
from pathlib import Path
import random
import urllib.request
from urllib.error import HTTPError, URLError
from http.client import RemoteDisconnected

dataset = Path('news2016.json').read_text().splitlines()
random.shuffle(dataset)

def download(document):
    url = document['url']
    if not url:
        return 'Missing URL'
    try:
        with urllib.request.urlopen(url) as source:
            html = source.read().decode('utf-8')
            filename.write_text(html)
        return "Downloaded"
    except HTTPError:
        return "Bad URL"
    except URLError:
        return "URL error"
    except RemoteDisconnected:
        "Remote end closed connection without response"
    except UnicodeDecodeError:
        return 'Non-utf-8 encoding'

with open('log.csv', 'a') as target:
    log = csv.writer(target)
    for i, record in enumerate(dataset):
        document = json.loads(record)
        ident = document['_id']
        url = document['url']
        source = document['source']
        filename = Path(f'Articles/{ident}/{ident}.html')
        if filename.exists():
            result = 'Skipped'
        else:
            dirname = Path(f'Articles/{ident}')
            dirname.mkdir(exist_ok=True)
            result = download(document)
            log.writerow([ident, source, url, result])
            target.flush()
        print(i, ident, source, result)
