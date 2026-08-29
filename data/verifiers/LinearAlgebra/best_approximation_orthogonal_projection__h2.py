import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        W = witness['W']
        P = witness['P']
        x = witness['x']
        w = witness['w']
    except (KeyError, TypeError):
        return [False, False, False, False]
        
    def dist_sq(a, b):
        diff = a - b
        return sp.simplify(sum(c * sp.conjugate(c) for c in diff))
        
    # H_1: V is an inner product space
    # We verify this by checking that x and elements of W are vectors (sympy Matrices) of the same dimension.
    try:
        h1 = isinstance(x, sp.Matrix)
        if h1:
            for y in W:
                if not isinstance(y, sp.Matrix) or y.shape != x.shape:
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    # H_2: P is the orthogonal projection operator onto W
    # We check if P maps x to a closest point in W, and acts as the identity on W.
    try:
        Px = P(x) if callable(P) else P * x
        
        px_in_W = False
        for y in W:
            if dist_sq(Px, y) == 0:
                px_in_W = True
                break
                
        px_dist = dist_sq(x, Px)
        is_closest = True
        for y in W:
            if dist_sq(x, y) < px_dist:
                is_closest = False
                break
                
        acts_id = True
        for y in W:
            Py = P(y) if callable(P) else P * y
            if dist_sq(Py, y) != 0:
                acts_id = False
                break
                
        h2 = px_in_W and is_closest and acts_id
    except Exception:
        h2 = False
        
    # H_3: x is a vector in V
    try:
        h3 = isinstance(x, sp.Matrix)
    except Exception:
        h3 = False
        
    # ¬Q: There exists w in W such that w != Px and ||x - Px|| >= ||x - w||
    try:
        w_in_W = False
        for y in W:
            if dist_sq(w, y) == 0:
                w_in_W = True
                break
                
        w_neq_Px = dist_sq(w, Px) != 0
        
        w_dist = dist_sq(x, w)
        ineq_fails = bool(px_dist >= w_dist)
        
        neg_q = w_in_W and w_neq_Px and ineq_fails
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "H_2: P is the orthogonal projection operator onto W",
    "H_3: x is a vector in V",
    "¬Q: There exists w in W such that w != Px and ||x - Px|| >= ||x - w||"
]

N_HYP = 3
NEG_Q_INDEX = 3