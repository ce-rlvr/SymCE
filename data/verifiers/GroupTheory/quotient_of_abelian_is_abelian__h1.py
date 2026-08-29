import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings for witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    # H_1: N is a subgroup of G
    try:
        h1 = bool(N.is_subgroup(G))
    except Exception:
        h1 = False
        
    # ¬Q: The quotient group G/N is not an abelian group
    try:
        if not N.is_subgroup(G):
            neg_q = True
        else:
            # Check if N is a normal subgroup of G
            is_normal = True
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
            
            if not is_normal:
                # If N is not normal, G/N is not a group, hence not an abelian group
                neg_q = True
            else:
                # G/N is abelian iff the generators of G commute modulo N
                is_abelian = True
                for g1 in G.generators:
                    for g2 in G.generators:
                        # Commutator of g1 and g2
                        if (~g1 * ~g2 * g1 * g2) not in N:
                            is_abelian = False
                            break
                    if not is_abelian:
                        break
                neg_q = not is_abelian
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a subgroup of G",
    "¬Q: The quotient group G/N is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1