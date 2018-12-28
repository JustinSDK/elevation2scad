import decimal

def line2Evals(line):
    tokens = line.strip().split('  ')
    return {'lat': tokens[0], 'lng': tokens[1], 'elevation': tokens[2]}
   
def toPoints(rawData, ymin, inc, heightScale = 1):
    lat = decimal.Decimal(str(ymin))
    latInc = decimal.Decimal(str(inc))
    latRows = []
    points = []
    for rawEvel in rawData:
        point = {
            'x': float(rawEvel['lat']), 
            'y': float(rawEvel['lng']), 
            'z': float(rawEvel['elevation']) / 111000 * heightScale
        }
        if decimal.Decimal(rawEvel['lng']) == lat:
            latRows.append(point)
        else:
            points.append(latRows)
            lat = lat + latInc
            latRows = [point]
    return points

def sea(points, level):
    def processRow(rowPts):
        return [[point['x'], point['y'] , point['z'] if point['z'] > 0 else level / 100] for point in rowPts]
    return [processRow(rowPts) for rowPts in points]

def writeScad(filename, points, thickness):
    xoffset = -points[0][1][0];
    yoffset = -points[0][1][1];
    scadCode = f'''
include <line3d.scad>;
include <polyline3d.scad>;
include <hull_polyline3d.scad>;
include <function_grapher.scad>;

points = {str(points)};
thickness = {thickness / 100};
scale(100) translate([{xoffset}, {yoffset}, 0]) function_grapher(points, thickness);
'''

    with open(filename, 'w') as f:
        f.write(scadCode)

def points_from(data, ymin, inc, sea_level = 1, heightScale = 1, thickness = 1):
    with open(data) as f:
        rawData = [line2Evals(line) for line in f]
    return sea(toPoints(rawData, ymin, inc, heightScale), sea_level)
        
def gen_scad_from(data, ymin, inc, sea_level = 1, heightScale = 1, thickness = 1):
    points = points_from(data, ymin, inc, sea_level, heightScale)
    writeScad('evelation.scad', points, thickness) 
    
if __name__ == "__main__":
    ymin, yinc, thickness = 21.750, 0.015, -1
    gen_scad_from('elevations.dat', ymin, yinc, thickness)