import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        G, k = witness
    except Exception:
        return [False, False]
        
    # H1: k is a non-negative integer
    try:
        h1 = isinstance(k, int) and not isinstance(k, bool) and k >= 0
    except Exception:
        h1 = False
        
    # neg_Q: G^(k) is NOT a subgroup of gamma_{2^k}(G)
    try:
        if not hasattr(G, 'derived_series') or not hasattr(G, 'lower_central_series'):
            neg_q = False
        else:
            ds = G.derived_series()
            derived = ds[k] if k < len(ds) else ds[-1]
            
            lcs = G.lower_central_series()
            
            # Standard 1-indexed notation: gamma_m is lcs[m-1]
            idx_standard = max(0, 2**k - 1)
            gamma_standard = lcs[idx_standard] if idx_standard < len(lcs) else lcs[-1]
            
            # 0-indexed notation (common programming error): gamma_m is lcs[m]
            idx_0 = 2**k
            gamma_0 = lcs[idx_0] if idx_0 < len(lcs) else lcs[-1]
            
            is_sub_standard = all(gen in gamma_standard for gen in derived.generators)
            is_sub_0 = all(gen in gamma_0 for gen in derived.generators)
            
            # The conclusion FAILS if it is not a subgroup under either interpretation
            neg_q = not (is_sub_standard and is_sub_0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is a non-negative integer",
    "¬Q: The k-th derived subgroup G^(k) is NOT a subgroup of gamma_{2^k}(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1