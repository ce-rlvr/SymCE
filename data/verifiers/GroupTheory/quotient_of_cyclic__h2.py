import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, N = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: G is a cyclic group
    try:
        h1 = bool(G.is_cyclic)
    except Exception:
        h1 = False

    # neg_Q: The quotient group G/N is not a cyclic group
    try:
        is_cyclic_quotient = False
        # For G/N to be a cyclic group, N must first be a normal subgroup of G.
        if hasattr(N, 'is_subgroup') and N.is_subgroup(G):
            if hasattr(G, 'is_normal') and G.is_normal(N):
                # If G is cyclic, any quotient by a normal subgroup is cyclic.
                if getattr(G, 'is_cyclic', False):
                    is_cyclic_quotient = True
                else:
                    # Manually check if G/N is cyclic by finding a generator
                    index = G.order() // N.order()
                    try:
                        elements = list(G.generate())
                    except Exception:
                        elements = list(G.elements)
                    
                    for g in elements:
                        k = 1
                        curr = g
                        while k <= index:
                            if curr in N:
                                break
                            curr = curr * g
                            k += 1
                        if k == index:
                            is_cyclic_quotient = True
                            break
                            
        neg_q = not is_cyclic_quotient
    except Exception:
        # If any operation fails (e.g., N is not a group), G/N is not a valid cyclic group.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: The quotient group G/N is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1