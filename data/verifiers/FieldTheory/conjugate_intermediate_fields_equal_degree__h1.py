import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: M_1 and M_2 are intermediate fields between K and L",
    "H_2: There exists a K-automorphism sigma in Aut(L/K) such that sigma(M_1) = M_2",
    "¬Q: The field extension degrees of M_1 over K and M_2 over K are not equal"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("h1", False))
            h2 = bool(witness.get("h2", False))
            neg_q = bool(witness.get("neg_q", False))
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            G, H1, H2, g = witness
            if hasattr(H1, 'is_subgroup'):
                h1 = H1.is_subgroup(G) and H2.is_subgroup(G)
                h2 = g in G
                if h2:
                    conj_elements = set((g * h * g**-1) for h in H1.elements)
                    h2_elements = set(H2.elements)
                    h2 = (conj_elements == h2_elements)
                
                deg1 = G.order() / H1.order()
                deg2 = G.order() / H2.order()
                neg_q = (deg1 != deg2)
                return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            return [bool(witness[0]), bool(witness[1]), bool(witness[2])]
    except Exception:
        pass

    try:
        if isinstance(witness, list) and len(witness) == 3:
            return [bool(witness[0]), bool(witness[1]), bool(witness[2])]
    except Exception:
        pass

    return [False, False, False]