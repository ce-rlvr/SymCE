import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
        G, phi, g, n = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: phi is an automorphism of G
    try:
        h2 = False
        if isinstance(G, PermutationGroup):
            elements = list(G.elements)
            if isinstance(phi, dict):
                mapping = phi
            elif callable(phi):
                mapping = {x: phi(x) for x in elements}
            else:
                mapping = None
            
            if mapping is not None:
                if len(mapping) == len(elements) and all(k in elements for k in mapping.keys()):
                    if set(mapping.values()) == set(elements):
                        is_hom = True
                        for x in elements:
                            for y in elements:
                                if mapping[x * y] != mapping[x] * mapping[y]:
                                    is_hom = False
                                    break
                            if not is_hom:
                                break
                        h2 = is_hom
    except Exception:
        h2 = False

    # neg_Q: phi(g) does not have order exactly n in G
    try:
        neg_q = False
        if isinstance(G, PermutationGroup):
            elements = list(G.elements)
            if g in elements and isinstance(n, (int, sympy.Integer)):
                if isinstance(phi, dict):
                    val = phi.get(g)
                elif callable(phi):
                    val = phi(g)
                else:
                    val = None
                
                if val is not None and val in elements:
                    neg_q = (val.order() != n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: phi is an automorphism of G",
    "¬Q: phi(g) does not have order exactly n in G"
]

N_HYP = 2
NEG_Q_INDEX = 2