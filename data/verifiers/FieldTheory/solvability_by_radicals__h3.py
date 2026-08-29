import sympy
from sympy import Poly, solveset, CRootOf, QQ
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

CONDITION_LABELS = [
    "H_1: F is a field of characteristic zero",
    "H_2: f(x) is a polynomial over F",
    "¬Q: f(x) is solvable by radicals over F iff Gal(K/F) is solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            f = witness.get('f')
            K = witness.get('K_poly', witness.get('K'))
        else:
            F, f, K = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = False
        if F == QQ:
            h1 = True
        elif hasattr(F, 'char') and F.char == 0:
            h1 = True
        elif hasattr(F, 'characteristic') and F.characteristic() == 0:
            h1 = True
    except Exception:
        h1 = False

    try:
        poly_f = Poly(f)
        if len(poly_f.free_symbols) > 1:
            h2 = False
        else:
            if F == QQ:
                h2 = all(c.is_rational for c in poly_f.coeffs())
            else:
                h2 = True
    except Exception:
        h2 = False

    try:
        def check_solvable(obj):
            if obj == QQ:
                return True
            if hasattr(obj, 'is_solvable'):
                val = obj.is_solvable
                if callable(val):
                    return val()
                return val
            p_expr = Poly(obj).as_expr()
            free = p_expr.free_symbols
            if not free:
                return True
            var = list(free)[0]
            roots = solveset(p_expr, var)
            return not any(isinstance(r, CRootOf) for r in roots)
        
        f_solvable = check_solvable(f)
        K_solvable = check_solvable(K)
        
        neg_q = bool(f_solvable != K_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]