import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
        # The witness must be a pair (G, N) where G is a group and N is a subgroup
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a finite group (and N is a valid subgroup of G)
    try:
        h1_ok = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            is_sub = True
            for gen in N.generators:
                if gen not in G:
                    is_sub = False
                    break
            if is_sub:
                order = G.order()
                if order != sympy.oo and order != float('inf'):
                    h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The order of the quotient group G/N is equal to |G| / |N|
    # Negation: The quotient group G/N does not exist (e.g., N is not normal) or its order is not |G|/|N|.
    try:
        neg_q_ok = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            is_normal = True
            if hasattr(G, 'is_normal'):
                is_normal = G.is_normal(N)
            else:
                # Manual fallback check for normality
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            is_normal = False
                            break
                        if (~g * n * g) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            # If N is not normal, the quotient group G/N does not exist, so the conclusion fails.
            # If N is normal, the quotient group exists and its order is exactly |G|/|N| by Lagrange's theorem.
            if not is_normal:
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The quotient group G/N does not exist or its order is not |G| / |N|"
]

N_HYP = 1
NEG_Q_INDEX = 1