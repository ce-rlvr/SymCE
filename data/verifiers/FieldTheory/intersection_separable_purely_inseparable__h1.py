import sympy
import sympy.abc
import sympy.polys
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory
import math
import itertools
import functools
import z3

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

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    try:
        E, F = witness
    except Exception:
        return [False, False, False]
        
    x_sym = sympy.Symbol('x')
    
    p_poly = None
    try:
        # Try to interpret E as a polynomial over F
        p_poly = sympy.Poly(E, x_sym, domain=F)
    except Exception:
        pass
        
    if p_poly is None or p_poly.degree() <= 0:
        try:
            # If E is an element, find its minimal polynomial over F
            p = sympy.minpoly(E, x_sym, domain=F)
            p_poly = sympy.Poly(p, x_sym, domain=F)
        except Exception:
            p_poly = None

    # H1: E is separable over F
    try:
        if p_poly is None:
            h1_ok = False
        else:
            gcd_poly = p_poly.gcd(p_poly.diff(x_sym))
            h1_ok = gcd_poly.degree() == 0
    except Exception:
        h1_ok = False
        
    # H2: E is purely inseparable over F
    try:
        if p_poly is None:
            h2_ok = False
        else:
            # A minimal polynomial is purely inseparable iff its degree is 1 
            # or its derivative is 0 (in characteristic p).
            if p_poly.degree() == 1:
                h2_ok = True
            elif p_poly.diff(x_sym) == 0 and p_poly.degree() > 0:
                h2_ok = True
            else:
                h2_ok = False
    except Exception:
        h2_ok = False
        
    # ¬Q: E is not equal to F
    try:
        q = (E == F)
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: E is separable over F",
    "H_2: E is purely inseparable over F",
    "¬Q: E is not equal to F"
]

N_HYP = 2
NEG_Q_INDEX = 2