import sympy
from sympy import eye, zeros
import z3
import itertools
import functools
import math

# Top-level setup for common rings
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12
ZZ = 0
QQ = 0

def parse_witness(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                m, X, Y = witness
                return int(m), list(X), list(Y)
            elif len(witness) == 2:
                m, pts = witness
                if isinstance(m, int):
                    if isinstance(pts, dict):
                        return int(m), list(pts.keys()), list(pts.values())
                    else:
                        return int(m), [p[0] for p in pts], [p[1] for p in pts]
                else:
                    return 0, list(m), list(pts)
        elif isinstance(witness, dict):
            return 0, list(witness.keys()), list(witness.values())
        elif isinstance(witness, list):
            return 0, [p[0] for p in witness], [p[1] for p in witness]
    except Exception:
        pass
    return None, None, None

def count_solutions(m, X, Y):
    try:
        n = len(X) - 1
        if n < 0:
            return 0
        solver = z3.Solver()
        solver.set("timeout", 2000)
        C = [z3.Int(f'c_{i}') for i in range(n+1)]
        
        if m > 0:
            for c in C:
                solver.add(c >= 0, c < m)
                
        for x, y in zip(X, Y):
            val = C[0]
            for i in range(1, n+1):
                val += C[i] * (int(x)**i)
            if m > 0:
                solver.add(val % m == int(y) % m)
            else:
                solver.add(val == int(y))
                
        res = solver.check()
        if res == z3.sat:
            model = solver.model()
            sol = [model[c].as_long() for c in C]
            diff_cond = z3.Or([c != sol[i] for i, c in enumerate(C)])
            solver.add(diff_cond)
            res2 = solver.check()
            if res2 == z3.sat:
                return 2
            elif res2 == z3.unsat:
                return 1
            else:
                return -1
        elif res == z3.unsat:
            return 0
        else:
            return -1
    except Exception:
        return -1

def conditions(witness):
    try:
        m, X, Y = parse_witness(witness)
        if X is None or Y is None:
            return [False, False, False]
            
        X = [int(x) for x in X]
        Y = [int(y) for y in Y]
        
        if m < 0:
            m = -m
            
        if m > 0:
            X_mod = [x % m for x in X]
            h1 = (len(set(X_mod)) == len(X)) and len(X) > 0
        else:
            h1 = (len(set(X)) == len(X)) and len(X) > 0
            
        h2 = (len(X) == len(Y))
        
        sols = count_solutions(m, X, Y)
        if sols == -1:
            neg_q = False
        else:
            neg_q = (sols != 1)
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: x_0 to x_n are n+1 distinct elements of K",
    "H_2: y_0 to y_n are elements of K",
    "not Q: There does not exist a unique polynomial P(x) over K with degree <= n such that P(x_i) = y_i for all i"
]

N_HYP = 2
NEG_Q_INDEX = 2