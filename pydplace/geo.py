# coding: utf8
from __future__ import unicode_literals, print_function, division

try:
    from shapely.geometry import shape
except ImportError:
    shape = None


def match(point, features):
    mindist, nearest = None, None
    for feature in features:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature, 0

        dist = point.distance(polygon)
        if mindist is None or mindist > dist:
            mindist, nearest = dist, feature

    assert mindist is not None
    return nearest, mindist
