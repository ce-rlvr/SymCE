import sympy
from sympy import Interval, FiniteSet, Union, Intersection, oo, ProductSet, Point
import math
import itertools

# Top-level setup for Real Analysis
R = sympy.S.Reals
Z = sympy.S.Integers
N = sympy.S.Naturals
N0 = sympy.S.Naturals0

def is_point(p):
    if isinstance(p, (int, float)):
        return True
    if hasattr(p, 'is_real') and p.is_real:
        return True
    if isinstance(p, (tuple, list)):
        return len(p) > 0 and all(is_point(x) for x in p)
    if isinstance(p, sympy.geometry.Point):
        return True
    return False

def closest_point_1d(p, K):
    if K == sympy.EmptySet:
        return []
    if K == sympy.S.Reals:
        return [p]
    if K == sympy.S.Integers or K == sympy.S.Naturals or K == sympy.S.Naturals0:
        try:
            p_val = float(p)
            lower = math.floor(p_val)
            upper = math.ceil(p_val)
            
            if K == sympy.S.Naturals:
                if upper < 1:
                    return [sympy.Integer(1)]
                lower = max(1, lower)
            elif K == sympy.S.Naturals0:
                if upper < 0:
                    return [sympy.Integer(0)]
                lower = max(0, lower)
                
            if p_val - lower < upper - p_val:
                return [sympy.Integer(lower)]
            elif upper - p_val < p_val - lower:
                return [sympy.Integer(upper)]
            else:
                if lower == upper:
                    return [sympy.Integer(lower)]
                return list(set([sympy.Integer(lower), sympy.Integer(upper)]))
        except Exception:
            return []
            
    if isinstance(K, Interval):
        if K.contains(p) == sympy.true:
            return [p]
        else:
            d1 = abs(p - K.start) if K.start != -oo else oo
            d2 = abs(p - K.end) if K.end != oo else oo
            if d1 < d2:
                return [K.start]
            elif d2 < d1:
                return [K.end]
            else:
                return [K.start, K.end]
    elif isinstance(K, FiniteSet):
        min_d = min(abs(p - x) for x in K)
        return [x for x in K if abs(p - x) == min_d]
    elif isinstance(K, Union):
        pts = []
        for arg in K.args:
            pts.extend(closest_point_1d(p, arg))
        if not pts:
            return []
        min_d = min(abs(p - x) for x in pts)
        return list(set([x for x in pts if abs(p - x) == min_d]))
    else:
        raise ValueError("Unsupported set type")

def closest_points_nd(p, K):
    if K == sympy.EmptySet:
        return []
    if isinstance(p, sympy.geometry.Point):
        p = p.coordinates
    if isinstance(p, (tuple, list)) and len(p) == 1 and not isinstance(K, (ProductSet, FiniteSet)):
        p = p[0]
    
    if isinstance(p, (int, float)) or (hasattr(p, 'is_real') and p.is_real):
        return closest_point_1d(p, K)
    
    if isinstance(K, ProductSet):
        if len(p) != len(K.sets):
            raise ValueError("Dimension mismatch")
        pts_per_dim = [closest_point_1d(pi, Ki) for pi, Ki in zip(p, K.sets)]
        return list(itertools.product(*pts_per_dim))
    elif isinstance(K, FiniteSet):
        min_dist = oo
        best_pts = []
        for x in K:
            if isinstance(x, sympy.geometry.Point):
                x_coords = x.coordinates
            elif isinstance(x, (int, float)) or (hasattr(x, 'is_real') and x.is_real):
                x_coords = (x,)
            else:
                x_coords = x
            
            if len(p) != len(x_coords):
                continue
                
            dist = sympy.sqrt(sum((pi - xi)**2 for pi, xi in zip(p, x_coords)))
            if dist < min_dist:
                min_dist = dist
                best_pts = [x_coords]
            elif dist == min_dist:
                if x_coords not in best_pts:
                    best_pts.append(x_coords)
        return best_pts
    elif isinstance(K, Union):
        pts = []
        for arg in K.args:
            try:
                pts.extend(closest_points_nd(p, arg))
            except Exception:
                pass
        if not pts:
            return []
        
        min_dist = oo
        best_pts = []
        for x_coords in pts:
            dist = sympy.sqrt(sum((pi - xi)**2 for pi, xi in zip(p, x_coords)))
            if dist < min_dist:
                min_dist = dist
                best_pts = [x_coords]
            elif dist == min_dist:
                if x_coords not in best_pts:
                    best_pts.append(x_coords)
        return best_pts
    else:
        raise ValueError("Unsupported set type")

def is_in_K(q, K):
    try:
        if isinstance(K, ProductSet):
            for qi, Ki in zip(q, K.sets):
                if Ki.contains(qi) != sympy.true:
                    return False
            return True
        elif isinstance(K, FiniteSet):
            return q in K
        else:
            if isinstance(q, (tuple, list)) and len(q) == 1:
                q = q[0]
            return K.contains(q) == sympy.true
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        p, K = witness
    except Exception:
        return [False, False]
    
    # H_1: p is a point in R^n
    try:
        h1 = is_point(p)
    except Exception:
        h1 = False
        
    # neg_Q: There does NOT exist q in K such that ||p - q|| = inf_{x in K} ||p - x||
    try:
        if not isinstance(K, sympy.Set):
            neg_q = False
        else:
            c_pts = closest_points_nd(p, K)
            if not c_pts:
                neg_q = True
            else:
                any_in_K = any(is_in_K(q, K) for q in c_pts)
                neg_q = not any_in_K
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a point in R^n",
    "¬Q: There does not exist a point q in K such that ||p - q|| = inf_{x in K} ||p - x||"
]

N_HYP = 1
NEG_Q_INDEX = 1