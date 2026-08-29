import sympy
import math
import itertools
import functools
from sympy.abc import x

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: For all x in the interval, f(x) is not equal to 0",
    "¬Q: f takes both positive and negative values"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False]
        f, a, b = witness
        a = float(a)
        b = float(b)
        if a >= b:
            return [False, False]
    except Exception:
        return [False, False]
        
    n_points = 1000
    grid = [a + (b - a) * i / float(n_points) for i in range(n_points + 1)]
    
    if a < 0 < b:
        grid.extend([0.0, -1e-9, 1e-9])
    grid.append(a + (b - a) * math.sqrt(2) / 2)
    
    h1_ok = True
    has_pos = False
    has_neg = False
    
    try:
        for val in grid:
            if callable(f):
                v = float(f(val))
            elif hasattr(f, 'subs'):
                v = float(f.subs(x, val))
            else:
                v = float(f)
                
            if v == 0.0:
                h1_ok = False
            elif v > 0:
                has_pos = True
            elif v < 0:
                has_neg = True
                
            if not h1_ok and has_pos and has_neg:
                break
    except Exception:
        h1_ok = False
        
    neg_q_ok = has_pos and has_neg
    
    return [h1_ok, neg_q_ok]