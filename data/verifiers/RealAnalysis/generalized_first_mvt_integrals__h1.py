import sympy
from sympy.abc import x
import math
import itertools
import functools

from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def has_solution(f, V, a, b):
    try:
        sol = sympy.solveset(f - V, x, domain=sympy.Interval(a, b))
        if sol is sympy.EmptySet:
            return False
        if isinstance(sol, sympy.Set) and not isinstance(sol, sympy.ConditionSet):
            if sol.is_empty == False:
                return True
            try:
                if len(sol) > 0:
                    return True
            except Exception:
                pass
    except Exception:
        pass

    try:
        n_samples = 1000
        y_vals = []
        for i in range(n_samples + 1):
            val_x = float(a) + float(b - a) * i / n_samples
            y_vals.append(float(f.subs(x, val_x)))
        
        for i in range(n_samples):
            y1 = y_vals[i]
            y2 = y_vals[i+1]
            
            if abs(y1 - V) < 1e-7 or abs(y2 - V) < 1e-7:
                return True
                
            if (y1 < V < y2) or (y2 < V < y1):
                if abs(y1 - y2) < 0.1:
                    return True
                else:
                    xa = float(a) + float(b - a) * i / n_samples
                    xb = float(a) + float(b - a) * (i + 1) / n_samples
                    ya, yb = y1, y2
                    for _ in range(20):
                        xm = (xa + xb) / 2.0
                        ym = float(f.subs(x, xm))
                        if abs(ym - V) < 1e-7:
                            return True
                        if (ya < V < ym) or (ym < V < ya):
                            xb, yb = xm, ym
                        else:
                            xa, ya = xm, ym
                    if abs(ya - yb) < 0.1:
                        return True
    except Exception:
        return True
        
    return False

def conditions(witness):
    try:
        f, g, a, b = witness
    except Exception:
        return [False, False, False]
    
    try:
        int_g = sympy.integrate(g, (x, a, b))
        if int_g.has(sympy.Integral):
            h1 = False
        else:
            try:
                float(int_g)
                h1 = True
            except Exception:
                h1 = False
    except Exception:
        h1 = False

    try:
        n_samples = 1000
        vals = []
        for i in range(n_samples + 1):
            val_x = float(a) + float(b - a) * i / n_samples
            val = float(g.subs(x, val_x))
            vals.append(val)
        has_pos = any(v > 1e-9 for v in vals)
        has_neg = any(v < -1e-9 for v in vals)
        h2 = not (has_pos and has_neg)
    except Exception:
        h2 = False

    try:
        int_fg = sympy.integrate(f * g, (x, a, b))
        if int_fg.has(sympy.Integral):
            neg_q = False
        else:
            try:
                I = float(int_fg)
                J = float(int_g)
            except Exception:
                neg_q = False
                return [bool(h1), bool(h2), bool(neg_q)]
            
            if abs(J) < 1e-9:
                if abs(I) < 1e-9:
                    neg_q = False
                else:
                    neg_q = True
            else:
                V = I / J
                if has_solution(f, V, a, b):
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = ["H_1: g is an integrable function", "H_2: g does not change sign", "neg_Q: There is no c such that integral equals f(c) times integral of g"]

N_HYP = 2
NEG_Q_INDEX = 2