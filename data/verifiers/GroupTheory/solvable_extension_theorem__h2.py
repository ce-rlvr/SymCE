import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture:
    "If G is a group, N is a solvable group, and G/N is a solvable group, then G is solvable."
    (The dropped hypothesis from the true theorem was "N is a normal subgroup of G").
    """
    try:
        G = witness[0]
        N = witness[1]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1_ok = hasattr(G, 'is_solvable') and hasattr(G, 'quotient_group')
    except Exception:
        h1_ok = False

    # H_2: N is a solvable group
    try:
        h2_ok = hasattr(N, 'is_solvable') and bool(N.is_solvable)
    except Exception:
        h2_ok = False

    # H_3: G/N is a solvable group
    try:
        try:
            # If N is a normal subgroup, standard quotient group works
            Q = G.quotient_group(N)
        except Exception:
            # If N is not normal, G/N is mathematically not a group.
            # However, in contexts where this false conjecture is evaluated, 
            # G/N is often interpreted as the quotient by the normal closure of N.
            NC = G.normal_closure(N)
            Q = G.quotient_group(NC)
        h3_ok = hasattr(Q, 'is_solvable') and bool(Q.is_solvable)
    except Exception:
        h3_ok = False

    # ¬Q: G is not a solvable group (Conclusion fails)
    try:
        neg_q_ok = hasattr(G, 'is_solvable') and not bool(G.is_solvable)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a solvable group",
    "H_3: G/N is a solvable group",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3