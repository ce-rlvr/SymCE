import sympy
from sympy import Poly, Symbol
from sympy.abc import x, y, z

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    F = None
    poly = None
    
    try:
        if isinstance(witness, Poly):
            poly = witness
            F = poly.domain
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                F, f = witness
                if isinstance(f, Poly):
                    poly = f
                else:
                    if hasattr(f, 'free_symbols'):
                        free = list(f.free_symbols)
                    else:
                        free = []
                    if not free:
                        poly = Poly(f, Symbol('x'), domain=F)
                    else:
                        free = sorted(free, key=lambda s: s.name)
                        poly = Poly(f, *free, domain=F)
            elif len(witness) == 3:
                F, f, gens = witness
                if not isinstance(gens, (list, tuple)):
                    gens = [gens]
                poly = Poly(f, *gens, domain=F)
    except Exception:
        pass

    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    try:
        h2 = False
        if poly is not None and not poly.is_zero:
            h2 = bool(poly.is_irreducible)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if F is not None and poly is not None:
            is_field = bool(F.is_Field) and bool(poly.is_irreducible) and len(poly.gens) == 1
            neg_q = not is_field
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a non-zero irreducible polynomial over F",
    "¬Q: The quotient ring is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2