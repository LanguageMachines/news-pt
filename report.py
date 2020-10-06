from collections import defaultdict
import json
from pathlib import Path

class Statistics:
    def __init__(self):
        self.articles = 0
        self.has_html = 0
        self.has_kwd = 0

report = defaultdict(Statistics)

dataset = Path('news2016.json').read_text().splitlines()

for i, record in enumerate(dataset):
    print(i)
    document = json.loads(record)
    ident = document['_id']
    url = document['url']
    source = document['source']
    report[source].articles += 1
    dir = Path(f'Articles/{ident}')
    html_file = dir / f'{ident}.html'
    if (html_file).exists():
        report[source].has_html += 1
        json_file = html_file.with_suffix('.json')
        if json_file.exists():
            json_doc = json.loads(json_file.read_text())
            if json_doc['keywords']:
                report[source].has_kwd += 1

for source, stats in report.items():
    print(f'{source} {stats.articles} {stats.has_html} {stats.has_kwd}')
