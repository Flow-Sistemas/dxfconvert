import ezdxf
from shapely.geometry import LineString

def convert_dxf_to_geojson(file_path: str) -> dict:
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()
    
    features = []

    for entity in msp:
        if entity.dxftype() in ("LINE", "LWPOLYLINE", "POLYLINE"):
            points = []
            try:
                points = list(entity.points())
            except AttributeError:
                if hasattr(entity, 'start') and hasattr(entity, 'end'):
                    points = [entity.start, entity.end]

            if points:
                coords = [(p[0], p[1]) for p in points]
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coords
                    },
                    "properties": {}
                }
                features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }
