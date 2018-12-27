import decimal

def line2Evals(line):
    tokens = line.strip().split('  ')
    return {'lat': tokens[0], 'lng': tokens[1], 'elevation': tokens[2]}
   
def toPoints(rawData, ymin, inc):
    lat = decimal.Decimal(str(ymin))
    latInc = decimal.Decimal(str(inc))
    latRows = []
    points = []
    for rawEvel in rawData:
        point = {
            'x': float(rawEvel['lat']), 
            'y': float(rawEvel['lng']), 
            'z': float(rawEvel['elevation']) / 111000
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
        return [[point['x'], point['y'] , point['z'] if point['z'] > 0 else level] for point in rowPts]
    return [processRow(rowPts) for rowPts in points]

def writeScad(filename, points):
    scadCode = f'''
include <line3d.scad>;
include <polyline3d.scad>;
include <hull_polyline3d.scad>;
include <function_grapher.scad>;

points = {str(points)};
thickness = 0.02;
scale(111) translate([-119.75, -21.5, 0]) function_grapher(points, thickness);
'''

    with open(filename, 'w') as f:
        f.write(scadCode)

def gen_from(data, ymin, inc, sea_level):
    with open(data) as f:
        rawData = [line2Evals(line) for line in f]

    writeScad('evelation.scad', sea(toPoints(rawData, ymin, inc), sea_level))

if __name__ == "__main__":
    gen_from('elevations.dat', 21.750, 0.015, -0.02)