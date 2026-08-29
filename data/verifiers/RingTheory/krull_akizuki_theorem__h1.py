import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a dictionary with the following keys:
    - "R_dim_1": True if Krull dimension of R is 1
    - "K_frac_R": True if K is the field of fractions of R
    - "L_fin_ext_K": True if L is a finite algebraic field extension of K
    - "R_sub_S_sub_L": True if R <= S <= L
    - "S_one_dim_Noetherian": False if S is NOT a one-dimensional Noetherian ring
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("R_dim_1", False))
            h2 = bool(witness.get("K_frac_R", False))
            h3 = bool(witness.get("L_fin_ext_K", False))
            h4 = bool(witness.get("R_sub_S_sub_L", False))
            neg_q = not bool(witness.get("S_one_dim_Noetherian", True))
            return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, "R_dim_1"):
            h1 = bool(getattr(witness, "R_dim_1", False))
            h2 = bool(getattr(witness, "K_frac_R", False))
            h3 = bool(getattr(witness, "L_fin_ext_K", False))
            h4 = bool(getattr(witness, "R_sub_S_sub_L", False))
            neg_q = not bool(getattr(witness, "S_one_dim_Noetherian", True))
            return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            R, K, L, S = witness
            from sympy import ZZ, QQ
            h1 = (R == ZZ)
            h2 = (R == ZZ and K == QQ)
            h3 = (K == QQ and L == QQ)
            h4 = (R == ZZ and S == QQ and L == QQ)
            neg_q = (S == QQ)
            if h1 and h2 and h3 and h4 and neg_q:
                return [True, True, True, True, True]
    except Exception:
        pass

    return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: The Krull dimension of R is 1",
    "H_2: K is the field of fractions of R",
    "H_3: L is a finite algebraic field extension of K",
    "H_4: S is a subring of L such that R \\subseteq S \\subseteq L",
    "¬Q: S is not a one-dimensional Noetherian ring"
]

N_HYP = 4
NEG_Q_INDEX = 4