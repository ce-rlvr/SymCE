import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N) where G and N are SymPy PermutationGroup objects.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H_1: N is a normal subgroup of G
    try:
        h1 = False
        if hasattr(N, 'generators') and hasattr(G, 'generators'):
            # Check if N is a subgroup of G
            is_sub = True
            for n in N.generators:
                if n not in G:
                    is_sub = False
                    break
            
            # Check for normality: g * n * g^-1 in N for all generators
            if is_sub:
                h1 = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H_2: Aut(N) is trivial
    # For finite groups, the automorphism group is trivial if and only if the group order is 1 or 2.
    try:
        h2 = False
        if hasattr(N, 'order'):
            h2 = bool(N.order() <= 2)
    except Exception:
        h2 = False

    # neg_Q: N is NOT contained in the center of G, Z(G)
    # N is in Z(G) iff every generator of N commutes with every generator of G.
    try:
        neg_q = False
        if hasattr(N, 'generators') and hasattr(G, 'generators'):
            in_center = True
            for n in N.generators:
                for g in G.generators:
                    if n * g != g * n:
                        in_center = False
                        break
                if not in_center:
                    break
            neg_q = not in_center
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: Aut(N) is trivial",
    "¬Q: N is not contained in the center of G"
]

N_HYP = 2
NEG_Q_INDEX = 2