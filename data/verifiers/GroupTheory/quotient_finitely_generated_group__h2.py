import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy import eye, zeros
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
    """
    Given a witness (G, N), checks if it is a valid counterexample to the false conjecture:
    Hypothesis: G is a finitely generated group
    Conclusion: The quotient group G/N is finitely generated
    
    The conclusion fails (i.e., G/N is not a finitely generated group) if N is not a normal 
    subgroup of G, because in that case the quotient G/N is not even a group.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a finitely generated group (and N is a valid subgroup to form a quotient)
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            # All PermutationGroups are finite, hence finitely generated.
            h1 = True
            # N must be a subgroup of G for G/N to be considered.
            for h in N.generators:
                if h not in G:
                    h1 = False
                    break
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # neg_Q: The quotient group G/N is NOT finitely generated.
    # If N is normal, G/N is a valid group and since G is finite, G/N is finite (hence finitely generated).
    # If N is NOT normal, G/N is not a group, so it fails to be a finitely generated group.
    try:
        if h1:
            is_normal = True
            for g in G.generators:
                for h in N.generators:
                    # Check closure under conjugation
                    if (g * h * ~g) not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "¬Q: The quotient group G/N is not finitely generated"
]

N_HYP = 1
NEG_Q_INDEX = 1