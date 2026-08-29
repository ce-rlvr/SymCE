import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H, K = witness
        else:
            G = witness.G
            H = witness.H
            K = witness.K
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup) or hasattr(G, 'quotient_group') or hasattr(G, '__truediv__')
    except Exception:
        h1_ok = False

    # H_2: The quotient group G/H is solvable
    try:
        if hasattr(G, 'quotient_group'):
            Q_H = G.quotient_group(H)
        else:
            Q_H = G / H
        h2_ok = bool(Q_H.is_solvable)
    except Exception:
        h2_ok = False

    # H_3: The quotient group G/K is solvable
    try:
        if hasattr(G, 'quotient_group'):
            Q_K = G.quotient_group(K)
        else:
            Q_K = G / K
        h3_ok = bool(Q_K.is_solvable)
    except Exception:
        h3_ok = False

    # neg_Q: The quotient group G/(H \cap K) is not solvable
    try:
        if hasattr(H, 'intersection'):
            H_int_K = H.intersection(K)
        elif hasattr(H, 'intersect'):
            H_int_K = H.intersect(K)
        else:
            H_int_K = H & K
            
        if hasattr(G, 'quotient_group'):
            Q_int = G.quotient_group(H_int_K)
        else:
            Q_int = G / H_int_K
            
        neg_q_ok = not bool(Q_int.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The quotient group G/H is solvable",
    "H_3: The quotient group G/K is solvable",
    "¬Q: The quotient group G/(H \\cap K) is not solvable"
]

N_HYP = 3
NEG_Q_INDEX = 3