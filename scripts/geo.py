import csv

import fiona
from shapely.geometry import shape, Point


def match(societies, regions):
    for society in societies:
        point = Point(float(society['Long']), float(society['Lat']))

        mindist, nearestregion = None, None
        for region in regions:
            polygon = shape(region['geometry'])
            if polygon.contains(point):
                yield society, region
                break
            dist = point.distance(polygon)
            if mindist is None or mindist > dist:
                mindist, nearestregion = dist, region
        else:
            assert mindist is not None
            print society['soc_id'], nearestregion['properties']['REGION_NAM'], mindist
            yield society, nearestregion


if __name__ == "__main__":
    with fiona.collection("../geo/level2-shape/level2.shp", "r") as source:
        regions = [f for f in source]

    with open("../csv/LatLong_data.csv") as fp:
        societies = list(csv.DictReader(fp))

    with open("../csv/society_region.csv", 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['soc_id', 'region', 'tdwg_code'])
        for soc, reg in match(societies, regions):
            writer.writerow([soc['soc_id'], reg['properties']['REGION_NAM'], reg['properties']['TDWG_CODE']])
