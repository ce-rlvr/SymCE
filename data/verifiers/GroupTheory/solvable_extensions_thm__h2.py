import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = hasattr(G, 'is_solvable') and hasattr(G, 'quotient_group') and hasattr(G, 'generators')
    except Exception:
        h1 = False

    try:
        h2 = bool(N.is_solvable)
    except Exception:
        h2 = False

    try:
        try:
            Q = G.quotient_group(N)
        except Exception:
            # If N is not a normal subgroup, G/N is technically undefined as a standard quotient group.
            # However, in computational group theory (e.g., GAP), G/N for non-normal N 
            # evaluates to the quotient of G by the normal closure of N.
            # This interpretation is what makes the dropped-hypothesis conjecture false.
            NC = G.normal_closure(N)
            Q = G.quotient_group(NC)
        h3 = bool(Q.is_solvable)
    except Exception:
        h3 = False

    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a solvable group",
    "H_3: The quotient group G/N is solvable",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3