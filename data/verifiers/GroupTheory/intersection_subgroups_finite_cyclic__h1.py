import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H, K), checks if it is a valid counterexample to the conjecture.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False]

    # H_1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h_sub = bool(H.is_subgroup(G))
        else:
            h_sub = all(g in G for g in H.generators)
    except Exception:
        h_sub = False

    # H_2: K is a subgroup of G
    try:
        if hasattr(K, 'is_subgroup'):
            k_sub = bool(K.is_subgroup(G))
        else:
            k_sub = all(g in G for g in K.generators)
    except Exception:
        k_sub = False

    # ¬Q: The order of H \cap K is not equal to gcd(|H|, |K|)
    try:
        try:
            h_elems = set(H.generate())
        except Exception:
            h_elems = set(H.elements)
            
        try:
            k_elems = set(K.generate())
        except Exception:
            k_elems = set(K.elements)
            
        int_order = len(h_elems.intersection(k_elems))
        expected = math.gcd(int(H.order()), int(K.order()))
        neg_q = (int_order != expected)
    except Exception:
        neg_q = False

    return [h_sub, k_sub, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of G",
    "¬Q: The order of H \\cap K is not equal to gcd(|H|, |K|)"
]

N_HYP = 2
NEG_Q_INDEX = 2