from collections import namedtuple

City = namedtuple('City', 'name country population coordinates')
LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
delhi = City._make(delhi_data)

for key, value in City._asdict(delhi).items():
    print(key + ':', value)


print(City._asdict(delhi))
print(City._fields)
print(delhi_data)
print(delhi)
