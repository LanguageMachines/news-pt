import html
import json
from pathlib import Path
import re

dataset = Path('news2016.json').read_text().splitlines()

def get_keywords(html_doc):
    keywords = set()
    for match in re.findall('<meta name=[\'"](news_)?keywords[\'"] content=[\'"]([^">]*)[\'"] */>', html_doc):
        content = html.unescape(match[1])
        if content:
            for keyword in content.split(','):
                keyword = keyword.strip()
                keywords.add(keyword)
    return sorted(keywords, key=lambda kwd: kwd.lower())

for i, record in enumerate(dataset):
    json_doc = json.loads(record)
    ident = json_doc['_id']
    url = json_doc['url']
    source = json_doc['source']
    filename = Path(f'Articles/{ident}/{ident}.html')
    if filename.exists():
        html_doc = filename.read_text()
        json_doc['keywords'] = get_keywords(html_doc)
        json_blob = json.dumps(json_doc)
        filename.with_suffix('.json').write_text(json_blob)
    print(i, ident)
