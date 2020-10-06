from collections import Counter
import json
from pathlib import Path

sources = Counter()
dataset = Path('news2016.json').read_text().splitlines()
for i, record in enumerate(dataset):
    document = json.loads(record)
    source = document['source']
    sources[source] += 1
print(sources)
print(len(sources))
