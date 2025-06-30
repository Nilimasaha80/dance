# src/angles.py
import math

def angle(a, b, c):
    ba = (a[0]-b[0], a[1]-b[1])
    bc = (c[0]-b[0], c[1]-b[1])
    cos = (ba[0]*bc[0] + ba[1]*bc[1]) / (math.hypot(*ba) * math.hypot(*bc))
    return math.degrees(math.acos(max(-1, min(1, cos))))
