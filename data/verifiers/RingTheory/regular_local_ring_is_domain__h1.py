import math
import itertools
import functools
import z3
import sympy
from sympy import Rational, Integer, Symbol
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

class AbstractRing:
    """
    A representation of an abstract ring for properties that cannot be 
    computationally verified in SymPy (e.g., non-Noetherian rings).
    """
    def __init__(self, is_local, max_ideal_gens, krull_dim, is_integral_domain):
        self.is_local = is_local
        self.max_ideal_gens = max_ideal_gens
        self.krull_dim = krull_dim
        self.is_integral_domain = is_integral_domain

def conditions(witness) -> list[bool]:
    # H_1: The ring R is a local ring with unique maximal ideal m.
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_local", False))
        else:
            h1 = bool(witness.is_local)
    except Exception:
        h1 = False

    # H_2: The minimal number of generators of the ideal m is equal to the Krull dimension of R.
    try:
        if isinstance(witness, dict):
            gens = witness.get("max_ideal_gens")
            dim = witness.get("krull_dim")
        else:
            gens = witness.max_ideal_gens
            dim = witness.krull_dim
        h2 = (gens is not None) and (dim is not None) and (gens == dim)
    except Exception:
        h2 = False

    # ¬Q: The ring R is not an integral domain.
    try:
        if isinstance(witness, dict):
            is_dom = witness.get("is_integral_domain", True)
        else:
            is_dom = witness.is_integral_domain
        neg_q = not bool(is_dom)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The ring R is a local ring with unique maximal ideal m",
    "H_2: The minimal number of generators of the ideal m is equal to the Krull dimension of R",
    "¬Q: The ring R is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2