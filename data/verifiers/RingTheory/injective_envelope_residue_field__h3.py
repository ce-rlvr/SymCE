import math
import itertools
import functools
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import Matrix

# Top-level setup
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
    "H_1: R is a commutative Noetherian local ring with maximal ideal m",
    "H_2: k = R/m is the residue field of R",
    "¬Q: E(k) is not an Artinian R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            is_comm = bool(witness.get("is_commutative", False))
            is_noeth = bool(witness.get("is_Noetherian", False) or witness.get("is_noetherian", False))
            is_local = bool(witness.get("is_local", False))
            h1 = is_comm and is_noeth and is_local
            
            h2 = bool(witness.get("is_residue_field", True))
            
            is_art = bool(witness.get("is_Artinian", True) or witness.get("is_artinian", True) or witness.get("E_k_is_Artinian", True))
            neg_q = not is_art
            return [h1, h2, neg_q]
        else:
            is_comm = bool(getattr(witness, "is_commutative", False))
            is_noeth = bool(getattr(witness, "is_Noetherian", False) or getattr(witness, "is_noetherian", False))
            is_local = bool(getattr(witness, "is_local", False))
            h1 = is_comm and is_noeth and is_local
            
            h2 = bool(getattr(witness, "is_residue_field", True))
            
            is_art = bool(getattr(witness, "is_Artinian", True) or getattr(witness, "is_artinian", True) or getattr(witness, "E_k_is_Artinian", True))
            neg_q = not is_art
            return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]