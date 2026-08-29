import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z, t

# Standard algebra objects
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

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "¬Q: The extension E/F is not a separable extension"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        poly = None
        if isinstance(witness, sp.Poly):
            poly = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], sp.Poly):
                poly = witness[0]
            elif isinstance(witness[1], sp.Poly):
                poly = witness[1]
            
        if poly is not None:
            # Check if the base field F is a finite field
            if hasattr(poly.domain, 'is_FiniteField'):
                h1 = bool(poly.domain.is_FiniteField)
            
            # An algebra E = F[x]/(P) over a perfect field F is a separable extension 
            # if and only if it is reduced, which means P is square-free.
            # Thus, the extension is NOT separable iff P is NOT square-free.
            neg_q = not bool(poly.is_sqf)
            
    except Exception:
        pass

    return [h1, neg_q]