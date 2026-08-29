import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, f, G = witness
            elif len(witness) == 2:
                F = sympy.QQ
                f, G = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = False
        if hasattr(F, 'char') and F.char == 0:
            h1 = True
        elif F in [sympy.QQ, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
    except Exception:
        h1 = False

    try:
        poly_f = sympy.Poly(f)
        h2 = poly_f.is_Poly and len(poly_f.gens) <= 1
    except Exception:
        h2 = False

    try:
        deg = poly_f.degree()
        if deg <= 4:
            f_solvable = True
        else:
            roots = sympy.solve(f)
            f_solvable = True
            for r in roots:
                if isinstance(r, sympy.RootOf) or type(r).__name__ == 'RootOf' or type(r).__name__ == 'ComplexRootOf':
                    f_solvable = False
                    break
                
        if hasattr(G, 'is_solvable'):
            g_solvable = bool(G.is_solvable)
        else:
            return [h1, h2, False]
            
        neg_q = (f_solvable != g_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic 0",
    "H_2: f(x) is a polynomial over F",
    "¬Q: f(x) is solvable by radicals iff Gal(E/F) is solvable is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2