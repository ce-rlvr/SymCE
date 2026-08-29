import sympy
from sympy import S, Interval, FiniteSet, Min, Max, sympify
from sympy.geometry import Polygon, Segment, Point, Ray, Line, convex_hull

# Top-level setup
R = S.Reals
Empty = S.EmptySet

def is_convex_set(s):
    if s == S.Reals or s == S.EmptySet:
        return True
    if isinstance(s, Interval):
        return True
    if isinstance(s, FiniteSet) and len(s) <= 1:
        return True
    if isinstance(s, Polygon):
        return s.is_convex()
    if isinstance(s, (Segment, Ray, Line, Point)):
        return True
    return False

def extreme_points(s):
    if s == S.Reals or s == S.EmptySet or isinstance(s, Line):
        return FiniteSet()
    if isinstance(s, Ray):
        return FiniteSet(s.source)
    if isinstance(s, FiniteSet) and len(s) <= 1:
        return s
    if isinstance(s, Point):
        return FiniteSet(s)
    if isinstance(s, Interval):
        ext = []
        if not s.left_open and s.start != S.NegativeInfinity:
            ext.append(s.start)
        if not s.right_open and s.end != S.Infinity:
            ext.append(s.end)
        return FiniteSet(*ext)
    if isinstance(s, Segment):
        return FiniteSet(*s.points)
    if isinstance(s, Polygon):
        if s.is_convex():
            return FiniteSet(*s.vertices)
    raise ValueError("Cannot determine extreme points")

def get_convex_hull(pts):
    if isinstance(pts, FiniteSet):
        if len(pts) == 0:
            return S.EmptySet
        if len(pts) == 1:
            p = list(pts)[0]
            if isinstance(p, Point):
                return p
            else:
                return FiniteSet(p)
        
        pts_list = [sympify(p) for p in pts]
        if all(hasattr(p, 'is_real') and p.is_real for p in pts_list):
            return Interval(Min(*pts_list), Max(*pts_list))
        if all(isinstance(p, Point) for p in pts_list):
            if len(pts_list) == 2:
                return Segment(*pts_list)
            return convex_hull(*pts_list)
    raise ValueError("Expected FiniteSet of points")

def are_equal(s1, s2):
    if s1 == s2:
        return True
    if isinstance(s1, Polygon) and isinstance(s2, Polygon):
        return set(s1.vertices) == set(s2.vertices)
    return False

def conditions(witness):
    try:
        h1 = bool(is_convex_set(witness))
    except Exception:
        h1 = False

    try:
        ext = extreme_points(witness)
        hull = get_convex_hull(ext)
        neg_q = not are_equal(witness, hull)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a convex set",
    "¬Q: K is not equal to the convex hull of its extreme points"
]

N_HYP = 1
NEG_Q_INDEX = 1