
import math


def get_decimal_degrees_to_webmerc(lon, lat):
    
    if abs(lon) > 180:
        raise ValueError('invalid longitude value')
    if abs(lat) > 90:
        raise ValueError('invalid latitude value')

    semimajorAxis = 6378137.0  # WGS84 spheriod semimajor axis
    east = lon * 0.017453292519943295
    north = lat * 0.017453292519943295

    northing = 3189068.5 * math.log((1.0 + math.sin(north)) / (1.0 - math.sin(north)))
    easting = semimajorAxis * east

    return (easting, northing)





    