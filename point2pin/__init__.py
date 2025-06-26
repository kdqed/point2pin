import gzip
import h3
import importlib.resources
import json
import os
from shapely.geometry import shape, Point

H3_RES = 7

H3_CELLS = json.loads(importlib.resources.read_text(
    'point2pin.indexes', 'h3_cells.json'
))
PIN_CODE_PROPS = json.loads(importlib.resources.read_text(
    'point2pin.indexes', 'pincodeprops.json'
))


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
            with importlib.resources.path(
                'point2pin.features', pincode + '.geojson.gz'
            ) as shapefile:
                with gzip.open(shapefile, 'rt') as f:
                    shapeobj = shape(json.loads(f.read()))
                    if shapeobj.contains(point):
                        return PIN_CODE_PROPS[pincode]
