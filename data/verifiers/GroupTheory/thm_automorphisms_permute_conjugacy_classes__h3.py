import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup for witness expressions
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
        G, phi, C = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: phi is an automorphism of G
    try:
        h2_ok = False
        if h1_ok:
            elements = list(G.generate_dimino())
            if isinstance(phi, dict):
                mapping = phi
            elif callable(phi):
                mapping = {x: phi(x) for x in elements}
            else:
                mapping = None
            
            if mapping is not None:
                # Check bijection
                if set(mapping.keys()) == set(elements) and set(mapping.values()) == set(elements):
                    # Check homomorphism
                    h2_ok = all(mapping[x * y] == mapping[x] * mapping[y] for x in elements for y in elements)
    except Exception:
        h2_ok = False

    # ¬Q: The image phi(C) is NOT a conjugacy class of G
    try:
        neg_q_ok = False
        if h1_ok and isinstance(C, (set, list, tuple, frozenset)):
            elements = set(G.generate_dimino())
            # Ensure C is a subset of G
            if all(x in elements for x in C):
                if isinstance(phi, dict):
                    phi_C = set(phi[x] for x in C)
                elif callable(phi):
                    phi_C = set(phi(x) for x in C)
                else:
                    phi_C = None
                
                if phi_C is not None:
                    if len(phi_C) > 0:
                        rep = next(iter(phi_C))
                        # Compute the actual conjugacy class of the representative in G
                        actual_class = set((g * rep * ~g) for g in elements)
                        # The conclusion fails if phi(C) is not exactly this conjugacy class
                        neg_q_ok = (phi_C != actual_class)
                    else:
                        # The empty set is not a conjugacy class
                        neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: phi is an automorphism of G",
    "¬Q: The image phi(C) is not a conjugacy class of G"
]

N_HYP = 2
NEG_Q_INDEX = 2