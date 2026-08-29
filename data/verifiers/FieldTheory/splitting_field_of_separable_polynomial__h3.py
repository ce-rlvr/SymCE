import sympy
from sympy import symbols, Poly
from sympy.polys.domains import GF, QQ
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        F = witness["F"]
        f = witness["f"]
        g = witness["g"]
        roots = witness["roots"]
        x = witness["x"]
        y = witness["y"]
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(f, sympy.Poly) and f.domain == F and f.degree() > 0 and f.gen == x
    except Exception:
        h2 = False
        
    try:
        h3 = False
        if isinstance(g, sympy.Poly) and g.domain == F and g.degree() > 0 and g.gen == y:
            coeffs = [sympy.Poly(1, y, domain=F)]
            for r in roots:
                new_coeffs = [sympy.Poly(0, y, domain=F) for _ in range(len(coeffs) + 1)]
                for i in range(len(coeffs)):
                    new_coeffs[i+1] = (new_coeffs[i+1] + coeffs[i]).rem(g)
                    term = (coeffs[i] * r).rem(g)
                    new_coeffs[i] = (new_coeffs[i] - term).rem(g)
                coeffs = new_coeffs
                
            f_coeffs = f.all_coeffs()
            f_coeffs.reverse()
            
            lc = f.LC()
            lc_poly = sympy.Poly(lc, y, domain=F)
            coeffs = [(c * lc_poly).rem(g) for c in coeffs]
            
            match = True
            if len(coeffs) != len(f_coeffs):
                match = False
            else:
                for c, fc in zip(coeffs, f_coeffs):
                    fc_poly = sympy.Poly(fc, y, domain=F)
                    if c != fc_poly:
                        match = False
                        break
                        
            y_poly = sympy.Poly(y, y, domain=F)
            generates = y_poly in roots
            
            if match and generates:
                h3 = True
    except Exception:
        h3 = False
        
    try:
        neg_q = False
        g_diff = g.diff(y)
        if g_diff.is_zero:
            neg_q = True
        else:
            try:
                gcd_g = g.gcd(g_diff)
                neg_q = gcd_g.degree() > 0
            except Exception:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a non-constant polynomial over F",
    "H_3: K is the splitting field of f over F",
    "not Q: The field extension K over F is not a Galois extension"
]

N_HYP = 3
NEG_Q_INDEX = 3