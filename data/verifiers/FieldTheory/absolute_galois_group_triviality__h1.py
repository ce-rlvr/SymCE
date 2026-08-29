import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

class AbstractField:
    """
    Represents a field with specific closure properties.
    """
    def __init__(self, is_algebraically_closed, is_separably_closed):
        self.is_algebraically_closed = is_algebraically_closed
        self.is_separably_closed = is_separably_closed

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            is_alg = bool(witness.get("is_algebraically_closed", False))
            is_sep = bool(witness.get("is_separably_closed", False))
            h1 = True
        elif hasattr(witness, "is_algebraically_closed") and hasattr(witness, "is_separably_closed"):
            is_alg = bool(witness.is_algebraically_closed)
            is_sep = bool(witness.is_separably_closed)
            h1 = True
        elif isinstance(witness, str):
            s = witness.lower()
            is_sep = "separably closed" in s or "separable closure" in s or "sep" in s
            is_alg = "algebraically closed" in s and "not algebraically closed" not in s
            h1 = True
        else:
            h1 = False
            return [False, False]
    except Exception:
        h1 = False
        return [False, False]

    try:
        # The absolute Galois group Gal(K^{sep}/K) is trivial 
        # if and only if K is separably closed (K = K^{sep}).
        galois_trivial = is_sep
        
        # Conclusion: K is algebraically closed iff Gal(K^{sep}/K) is trivial
        conclusion = (is_alg == galois_trivial)
        
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K^{sep} is a separable closure of K",
    "¬Q: The equivalence between K being algebraically closed and Gal(K^{sep}/K) being trivial fails"
]

N_HYP = 1
NEG_Q_INDEX = 1