import gzip
import os
import json

DIR = os.path.join('point2pin', 'features')
os.makedirs(DIR, exist_ok=True)

with open('boundaries.geojson') as f:
    features = json.loads(f.read())['features']

i = 0
for feature in features:
    i += 1
    print(i, end="\r"*5)
    with gzip.open(os.path.join(DIR, feature['properties']['Pincode'] + '.geojson.gz'), 'wt') as f:
        f.write(json.dumps(feature))

