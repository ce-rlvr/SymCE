import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            a = witness['a']
            b = witness['b']
        else:
            G, H, a, b = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: a is an element of G
    try:
        h2 = a in G
    except Exception:
        h2 = False

    # H_3: b is an element of G
    try:
        h3 = b in G
    except Exception:
        h3 = False

    # ¬Q: The left coset aH is equal to the left coset bH if and only if a^{-1}b is an element of H
    try:
        H_elements = list(H)
        aH = [a * h for h in H_elements]
        bH = [b * h for h in H_elements]
        
        try:
            eq_cosets = set(aH) == set(bH)
        except TypeError:
            # Fallback for unhashable elements
            eq_cosets = len(aH) == len(bH) and all(x in bH for x in aH) and all(x in aH for x in bH)
            
        try:
            a_inv = ~a
        except Exception:
            a_inv = a**-1
            
        a_inv_b = a_inv * b
        in_H = a_inv_b in H_elements
        
        # The conclusion is (aH == bH) <=> (a^{-1}b in H)
        # We want the negation of the conclusion
        neg_q = (eq_cosets != in_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: a is an element of G",
    "H_3: b is an element of G",
    "¬Q: (aH == bH) is not equivalent to (a^-1 b in H)"
]

N_HYP = 3
NEG_Q_INDEX = 3