import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
)

# Standard group bindings for the witness namespace
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def wreath_product(A, B):
    """
    Constructs the standard wreath product A wr B.
    A and B must be permutation groups.
    """
    dA = A.degree
    dB = B.degree
    if dA == 0: dA = 1
    if dB == 0: dB = 1
    
    gens = []
    # Base group generators (copies of A)
    for g in A.generators:
        for i in range(dB):
            perm = list(range(dA * dB))
            for j in range(dA):
                perm[i * dA + j] = i * dA + g(j)
            gens.append(Permutation(perm))
            
    # Top group generators (action of B)
    for h in B.generators:
        perm = list(range(dA * dB))
        for i in range(dB):
            hi = h(i)
            for j in range(dA):
                perm[i * dA + j] = hi * dA + j
        gens.append(Permutation(perm))
        
    if not gens:
        return PermutationGroup([Permutation(dA * dB - 1)])
    return PermutationGroup(gens)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness can be a tuple (A, B) or (A, B, G).
    """
    try:
        if len(witness) == 3:
            A, B, G = witness
        elif len(witness) == 2:
            A, B = witness
            G = wreath_product(A, B)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: B is a finite solvable group
    try:
        h1 = bool(B.is_solvable)
    except Exception:
        h1 = False

    # H_2: G is the wreath product of A and B
    try:
        if len(witness) == 2:
            h2 = True
        else:
            order_A = A.order() if callable(A.order) else A.order
            order_B = B.order() if callable(B.order) else B.order
            order_G = G.order() if callable(G.order) else G.order
            expected_order = (order_A ** B.degree) * order_B
            h2 = bool(order_G == expected_order)
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: B is a finite solvable group",
    "H_2: G is the wreath product of A and B",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2