import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness) -> list[bool]:
    if isinstance(witness, (tuple, list)) and len(witness) > 0:
        obj = witness[0]
    else:
        obj = witness

    p = None
    if isinstance(obj, sympy.Expr):
        free_syms = obj.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
            try:
                poly = sympy.poly(obj, sym)
                if sympy.simplify(obj - (sym**poly.degree() - 2)) == 0:
                    p = poly.degree()
            except Exception:
                pass
                
    if p is None:
        try:
            p = int(obj)
        except Exception:
            pass

    try:
        p_int = int(p)
        h1 = bool(p_int >= 1 and p == p_int)
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        p_int = int(p)
        neg_q = not sympy.isprime(p_int)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial",
    "H_2: L is the splitting field",
    "¬Q: Galois group is not the semidirect product"
]

N_HYP = 2
NEG_Q_INDEX = 2