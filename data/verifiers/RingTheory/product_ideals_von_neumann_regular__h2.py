import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            I = witness['I']
            J = witness['J']
            add = witness.get('add', lambda a, b: a + b)
            mul = witness.get('mul', lambda a, b: a * b)
            eq = witness.get('eq', lambda a, b: a == b)
        else:
            R, I, J = witness
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
            eq = lambda a, b: a == b
    except Exception:
        return [False, False, False]

    def contains(L, elem):
        return any(eq(y, elem) for y in L)

    def subset(L1, L2):
        return all(contains(L2, elem) for elem in L1)

    def set_eq(L1, L2):
        return subset(L1, L2) and subset(L2, L1)

    def unique(L):
        res = []
        for elem in L:
            if not contains(res, elem):
                res.append(elem)
        return res

    # H1: R is a von Neumann regular ring
    h1 = False
    try:
        if not R:
            raise ValueError
        
        zero = None
        for z_cand in R:
            if all(eq(add(z_cand, a), a) and eq(add(a, z_cand), a) for a in R):
                zero = z_cand
                break
        if zero is None:
            raise ValueError
            
        for a in R:
            for b in R:
                ab_add = add(a, b)
                ab_mul = mul(a, b)
                if not contains(R, ab_add): raise ValueError
                if not eq(ab_add, add(b, a)): raise ValueError
                if not contains(R, ab_mul): raise ValueError
                for c in R:
                    bc_add = add(b, c)
                    bc_mul = mul(b, c)
                    if not eq(add(ab_add, c), add(a, bc_add)): raise ValueError
                    if not eq(mul(ab_mul, c), mul(a, bc_mul)): raise ValueError
                    if not eq(mul(a, bc_add), add(ab_mul, mul(a, c))): raise ValueError
                    if not eq(mul(ab_add, c), add(mul(a, c), mul(b, c))): raise ValueError
                    
        for a in R:
            if not any(eq(add(a, b), zero) for b in R):
                raise ValueError
                
        for a in R:
            if not any(eq(mul(mul(a, x_elem), a), a) for x_elem in R):
                raise ValueError
                
        h1 = True
    except Exception:
        h1 = False

    # H2: J is a two-sided ideal of R
    h2 = False
    try:
        if not J:
            raise ValueError
        if not subset(J, R):
            raise ValueError
            
        for a in J:
            for b in J:
                if not contains(J, add(a, b)):
                    raise ValueError
            inv_a = None
            for x_elem in R:
                if eq(add(a, x_elem), zero):
                    inv_a = x_elem
                    break
            if not contains(J, inv_a):
                raise ValueError
                
        for r in R:
            for j in J:
                if not contains(J, mul(r, j)):
                    raise ValueError
                if not contains(J, mul(j, r)):
                    raise ValueError
                    
        h2 = True
    except Exception:
        h2 = False

    # Negated conclusion: IJ != I \cap J
    neg_q = False
    try:
        I_cap_J = [elem for elem in I if contains(J, elem)]
        
        generators = []
        for i in I:
            for j in J:
                generators.append(mul(i, j))
        
        IJ = unique(generators)
        if IJ:
            changed = True
            while changed:
                changed = False
                new_elements = []
                for x_elem in IJ:
                    for g in generators:
                        s = add(x_elem, g)
                        if not contains(IJ, s) and not contains(new_elements, s):
                            new_elements.append(s)
                if new_elements:
                    IJ.extend(new_elements)
                    changed = True
                if len(IJ) > len(R):
                    raise ValueError
                
        if not set_eq(IJ, I_cap_J):
            neg_q = True
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a von Neumann regular ring",
    "H_2: J is a two-sided ideal of R",
    "¬Q: IJ != I \\cap J"
]

N_HYP = 2
NEG_Q_INDEX = 2