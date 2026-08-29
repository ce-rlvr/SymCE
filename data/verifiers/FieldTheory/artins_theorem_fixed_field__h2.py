import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math

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

class ArtinWitness:
    def __init__(self, L_is_field, K_is_fixed_field, is_finite_galois, degree, G_order):
        self.L_is_field = bool(L_is_field)
        self.K_is_fixed_field = bool(K_is_fixed_field)
        self.is_finite_galois = bool(is_finite_galois)
        self.degree = degree
        self.G_order = G_order

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("L_is_field", False))
        else:
            h1 = bool(witness.L_is_field)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get("K_is_fixed_field", False))
        else:
            h2 = bool(witness.K_is_fixed_field)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            is_finite_galois = bool(witness.get("is_finite_galois", False))
            degree = witness.get("degree", float('inf'))
            G_order = witness.get("G_order", float('inf'))
        else:
            is_finite_galois = bool(witness.is_finite_galois)
            degree = witness.degree
            G_order = witness.G_order
            
        is_finite_degree = (degree is not None) and (degree != float('inf')) and (degree != math.inf)
        is_finite_G = (G_order is not None) and (G_order != float('inf')) and (G_order != math.inf)
        
        q = is_finite_galois and is_finite_degree and is_finite_G and (degree == G_order)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: L is a field", "H_2: K is the fixed field of G in L", "¬Q: L/K is not a finite Galois extension or degree is not G_order"]

N_HYP = 2
NEG_Q_INDEX = 2