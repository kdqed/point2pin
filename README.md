# Point2Pin: Python Library To Convert Latitude/Longitude To Indian Pincode

- Based on pin code boundaries from: https://www.data.gov.in/catalog/all-india-pincode-boundary-geo-json
- Accelerated lookups using H3 Indexing

## Installation

Using `pip`:

```
$ pip install point2pin
```

Using `uv`:

```
$ uv add point2pin
```

## Usage

```python
import point2pin

result = point2pin.lookup(12.9807806, 77.6421572) # (lat, lng)
print(result)

'''
OUTPUT:
{'Pincode': '560038', 'Office_Name': 'Indiranagar S.O (Bengaluru)', 'Division': 'Bengaluru East ', 'Region': 'Bengaluru HQ ', 'Circle': 'Karnataka '}
'''
```

## REST API

Contact [krtdvn@gmail.com](mailto:krtdvn@gmail.com) for hosted API quotes.
