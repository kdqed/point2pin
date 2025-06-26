import gzip
import h3
import json
import os
from pathlib import Path
from shapely.geometry import shape

H3_RES = 7
DIR = Path('point2pin') / 'indexes'

os.makedirs(DIR, exist_ok=True)
pincodeprops = {}
h3_cells = {}


def geom_to_h3_cells(geometry):
    h3shape = h3.geo_to_h3shape(geometry)
    interior_cells = h3.polygon_to_cells(h3shape, H3_RES)

    border_cells = set()
    ring_points = []
    if geometry["type"]=="Polygon":
        for ls in geometry["coordinates"]:
            ring_points += ls
    elif geometry["type"]=="MultiPolygon":
        for polygon in geometry["coordinates"]:
            for ls in polygon:
                ring_points += ls
                
    for point in ring_points:
        border_cells.add(h3.latlng_to_cell(point[1], point[0], H3_RES))

    return interior_cells + list(border_cells)


FEATURES_DIR = Path('point2pin') / 'features'
for pinfile in os.listdir(FEATURES_DIR):
    print(pinfile, end='\r'*30)
    with gzip.open(FEATURES_DIR / pinfile, 'rt') as f:
        feature = json.loads(f.read())
        pincodeprops[feature['properties']['Pincode']] = feature['properties']
        cells = geom_to_h3_cells(feature['geometry'])
        for cell in cells:
            if cell not in h3_cells:
                h3_cells[cell] = set()
            h3_cells[cell].add(feature['properties']['Pincode'])
        

pins_per_cell = {}
for cell in h3_cells:
    h3_cells[cell] = list(h3_cells[cell])
    length = len(h3_cells[cell])
    pins_per_cell[length] = pins_per_cell.get(length, 0) + 1 

print("Pins per cell:", pins_per_cell)

with open(DIR / 'pincodeprops.json', 'w') as f:
    f.write(json.dumps(pincodeprops))
    f.close()

with open(DIR / 'h3_cells.json', 'w') as f:
    f.write(json.dumps(h3_cells))
    f.close()
