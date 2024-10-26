import math


def calcMinDist(plobject, WIDTH, heightByX):
    minDist = None
    for coorX in range(plobject.radius * 2 + 1):
        px = (plobject.x - plobject.radius) + coorX
        if px < 0 or px > WIDTH:
            continue
        groundY = heightByX[int(px)]
        dx = plobject.radius - coorX
        dy = math.sqrt((plobject.radius ** 2) - (dx ** 2))
        py = plobject.y + dy
        dist = groundY - py
        if minDist is None or dist < minDist:
            minDist = dist
    return minDist


def HeightByXCreate(HEIGHT, WIDTH, func):
    heightByX = {}
    for i in range(0, WIDTH + 1):
        heightByX.update({i: HEIGHT - func(i)})
    return heightByX


def hbx2points(heightByX):
    points = []
    for i in range(0, len(heightByX)):
        points.append((i, heightByX[i]))
    return points


def calcSeg(startPoint: tuple, endPoint: tuple):
    points = {}
    sp = max(startPoint, endPoint)
    ep = min(startPoint, endPoint)
    length = abs(ep[0] - sp[0])
    if length > 0:
        for i in range(length + 1):
            t = i / length
            x = sp[0] + (ep[0] - sp[0]) * t
            y = sp[1] + (ep[1] - sp[1]) * t
            points.update({x: y})
        return points
    else:
        return {sp[0]: ep[1]}
