import gzip
import h3
import json
import os
from shapely.geometry import shape, Point

H3_RES = 7
PKG_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(PKG_DIR, 'indexes', 'h3_cells.json')) as f:
    H3_CELLS = json.loads(f.read())

with open(os.path.join(PKG_DIR, 'indexes', 'pincodeprops.json')) as f:
    PIN_CODE_PROPS = json.loads(f.read())

def lookup(lat: float, lng: float) -> dict | None:
    idx = h3.latlng_to_cell(lat, lng, H3_RES)
    candidates = H3_CELLS.get(idx)
    if candidates is None:
        return None

    if len(candidates)==1:
        return PIN_CODE_PROPS[candidates[0]]
    else:
        point = Point(lng, lat)
        for pincode in candidates:
            shapefile = os.path.join(PKG_DIR, 'features', pincode + '.geojson.gz')
            with gzip.open(shapefile, 'rt') as f:
                shapeobj = shape(json.loads(f.read()))
                if shapeobj.contains(point):
                    return PIN_CODE_PROPS[pincode]
