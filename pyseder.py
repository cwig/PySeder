import sys
import numpy as np

with open('sederstring.txt') as f:
    sederstring = f.read()

#Point is np.array([x,y,w])
class Curve(object):
    def __init__(self, points):
        self.degree = len(points) - 1
        self.points = points

def plotBezier(curve):
    pointlines = ["[{} {} {}]".format(*tuple(p)) for p in curve.points]
    return "[" + "".join(pointlines) + "] cplot"

def plotControlPolygon(curve):
    pointlines = ["{} {} mv ".format(*tuple(magicPoint(curve.points[0])))]
    for pt in curve.points[1:]:
        pointlines.append("{} {} ln ".format(*tuple(magicPoint(pt))))
    pointlines.append("stroke")
    return "".join(pointlines)

def magicPoint(pt):
    return pt[0]/pt[2], pt[1]/pt[2]

def readPoint(pt):
    return pt[0]*pt[2], pt[1]*pt[2], pt[2]

def main():
    if len(sys.argv) < 3:
        print "Syntax:\n python pyplot.py filename"
        return

    curves = {}
    output = [sederstring]

    with open(sys.argv[1]) as f:
        while True:
            line = f.readline().strip().lower()[:4]

            if line == "bord":
                output.append("border stroke")

            elif line == "cplo":
                nCurve = int(f.readline().strip().lower())
                output.append(plotBezier(curves[nCurve]))

            elif line == "circ":
                params = map(float, f.readline().strip().lower().split())
                output.append("{} {} {} circ".format(*params))

            elif line == "colo":
                params = map(float, f.readline().strip().lower().split())
                output.append("{} {} {} setrgbcolor".format(*params))

            elif line == "cppl":
                nCurve = int(f.readline().strip().lower())
                output.append(plotControlPolygon(curves[nCurve]))

            elif line == "exit":
                break

            elif line == "stor":
                nCurve = int(f.readline().strip().lower())
                degree = int(f.readline().strip().lower())
                pts = [readPoint(map(float, f.readline().strip().lower().split())) for v in xrange(degree+1)]
                curves[nCurve] = Curve(np.array(pts))

            elif line == "text":
                size, x, y = map(float, f.readline().strip().lower().split())
                text = f.readline().strip()
                output.append("{} {} mv /Times-Roman findfont {} scalefont setfont ({}) show".format(x,y,size,text))

            elif line == "view":
                params = map(float, f.readline().strip().lower().split())
                output.append("{} {} {} {} viewport".format(*params))

            elif line == "wind":
                params = map(float, f.readline().strip().lower().split())
                output.append("{} {} {} {} window".format(*params))

            elif line == "widt":
                size = int(f.readline().strip().lower())
                output.append("{} setlinewidth".format(size))

            elif line == "disp":
                for i in sorted(curves):
                    c = curves[i]
                    for p in c.points:
                        pass

            else:
                raise Exception("Illegal command: {}".format(line))


        with open(sys.argv[2], 'w') as f:
            f.write("\n".join(output)+"\n")

if __name__ == "__main__":
    main()
