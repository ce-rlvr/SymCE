import sympy
from sympy import Interval, FiniteSet, Union, S, oo
from sympy.abc import x, y, z

# Standard algebra objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is a non-empty subset of X",
    "H_2: A is compact",
    "H_3: B is a closed subset of X",
    "H_4: A and B are disjoint",
    "¬Q: The infimum of d(a, b) for all a in A and b in B is not strictly greater than zero"
]

N_HYP = 4
NEG_Q_INDEX = 4

def point_interval_distance(p, interval):
    if interval.start != -oo and p < interval.start:
        return interval.start - p
    elif interval.end != oo and p > interval.end:
        return p - interval.end
    else:
        return 0

def basic_set_distance(a, b):
    if isinstance(a, FiniteSet) and isinstance(b, FiniteSet):
        return min(abs(x - y) for x in a for y in b)
    if isinstance(a, FiniteSet) and isinstance(b, Interval):
        return min(point_interval_distance(x, b) for x in a)
    if isinstance(a, Interval) and isinstance(b, FiniteSet):
        return min(point_interval_distance(y, a) for y in b)
    if isinstance(a, Interval) and isinstance(b, Interval):
        if a.end != oo and b.start != -oo and a.end <= b.start:
            return b.start - a.end
        elif b.end != oo and a.start != -oo and b.end <= a.start:
            return a.start - b.end
        else:
            return 0
    if b == S.Integers:
        from sympy import floor, ceiling
        if isinstance(a, FiniteSet):
            return min(min(x - floor(x), ceiling(x) - x) for x in a)
        if isinstance(a, Interval):
            if a.end - a.start >= 1:
                return 0
            f = floor(a.start)
            c = ceiling(a.start)
            if a.start <= f <= a.end or a.start <= c <= a.end:
                return 0
            return min(a.start - floor(a.start), ceiling(a.end) - a.end)
    if a == S.Integers:
        return basic_set_distance(b, a)
    return oo

def set_distance(A, B):
    if A.is_empty or B.is_empty:
        return oo
    if not A.intersect(B).is_empty:
        return 0

    def get_basic_sets(S_set):
        if isinstance(S_set, Union):
            return S_set.args
        else:
            return [S_set]

    A_basics = get_basic_sets(A)
    B_basics = get_basic_sets(B)

    min_dist = oo
    for a in A_basics:
        for b in B_basics:
            d = basic_set_distance(a, b)
            if d < min_dist:
                min_dist = d
    return min_dist

def get_distance(A, B):
    if hasattr(A, 'distance'):
        try:
            return A.distance(B)
        except Exception:
            pass
    return set_distance(A, B)

def conditions(witness):
    try:
        if isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                A, B = witness
            elif len(witness) >= 3:
                A, B = witness[-2], witness[-1]
            else:
                return [False] * 5
        else:
            A = witness.A
            B = witness.B
    except Exception:
        return [False] * 5

    # H1: A is a non-empty subset of X
    try:
        if hasattr(A, 'is_empty'):
            a_empty = A.is_empty() if callable(getattr(A, 'is_empty', None)) else A.is_empty
            h1 = not bool(a_empty)
        else:
            geom_types = ('Point', 'Point2D', 'Point3D', 'Segment', 'Segment2D', 'Segment3D', 'Polygon', 'RegularPolygon', 'Triangle', 'Circle', 'Ellipse', 'Line', 'Line2D', 'Line3D', 'Ray', 'Ray2D', 'Ray3D')
            if type(A).__name__ in geom_types:
                h1 = True
            else:
                h1 = len(A) > 0
    except Exception:
        h1 = False

    # H2: A is compact
    try:
        if hasattr(A, 'is_closed') and hasattr(A, 'is_bounded'):
            a_closed = A.is_closed() if callable(getattr(A, 'is_closed', None)) else A.is_closed
            a_bounded = A.is_bounded() if callable(getattr(A, 'is_bounded', None)) else A.is_bounded
            h2 = bool(a_closed and a_bounded)
        else:
            geom_compact = ('Point', 'Point2D', 'Point3D', 'Segment', 'Segment2D', 'Segment3D', 'Polygon', 'RegularPolygon', 'Triangle', 'Circle', 'Ellipse')
            if type(A).__name__ in geom_compact:
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False

    # H3: B is a closed subset of X
    try:
        if hasattr(B, 'is_closed'):
            b_closed = B.is_closed() if callable(getattr(B, 'is_closed', None)) else B.is_closed
            h3 = bool(b_closed)
        else:
            geom_closed = ('Point', 'Point2D', 'Point3D', 'Segment', 'Segment2D', 'Segment3D', 'Polygon', 'RegularPolygon', 'Triangle', 'Circle', 'Ellipse', 'Line', 'Line2D', 'Line3D', 'Ray', 'Ray2D', 'Ray3D')
            if type(B).__name__ in geom_closed:
                h3 = True
            else:
                h3 = False
    except Exception:
        h3 = False

    # H4: A and B are disjoint
    try:
        if hasattr(A, 'is_disjoint'):
            h4 = bool(A.is_disjoint(B))
        elif hasattr(A, 'intersect'):
            inter = A.intersect(B)
            inter_empty = inter.is_empty() if callable(getattr(inter, 'is_empty', None)) else inter.is_empty
            h4 = bool(inter_empty)
        elif hasattr(A, 'intersection'):
            inter = A.intersection(B)
            h4 = len(inter) == 0
        else:
            h4 = set(A).isdisjoint(set(B))
    except Exception:
        h4 = False

    # neg_Q: The infimum of d(a, b) for all a in A and b in B is NOT strictly greater than zero.
    try:
        dist = None
        if isinstance(witness, (list, tuple)) and len(witness) == 4:
            d_func = witness[1]
            if callable(d_func):
                dist = min(d_func(a, b) for a in A for b in B)
        
        if dist is None:
            dist = get_distance(A, B)
            
        neg_q = bool(dist <= 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]