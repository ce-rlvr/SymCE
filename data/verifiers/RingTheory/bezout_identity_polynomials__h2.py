import sympy
from sympy import Poly, linsolve, symbols, gcd, cancel
from sympy.abc import x, y, z
from sympy import QQ, ZZ, RR, CC
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) and g(x) are relatively prime",
    "¬Q: There do not exist polynomials a(x), b(x) such that a(x)f(x) + b(x)g(x) = 1"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        F, f, g, var_x = witness
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        var_x = sympy.sympify(var_x)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False
        
    try:
        d = sympy.gcd(f, g)
        h2 = bool(d.is_number and d != 0)
    except Exception:
        h2 = False
        
    try:
        vars_all = list(f.free_symbols | g.free_symbols)
        if not vars_all:
            neg_q = False
        else:
            gb = sympy.groebner([f, g], *vars_all, domain=F)
            if len(gb) == 1 and gb[0] == 1:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]