import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            g = witness.get('g')
            h = witness.get('h')
            m = witness.get('m')
            n = witness.get('n')
        elif isinstance(witness, (list, tuple)) and len(witness) == 6:
            G, H, g, h, m, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: g is an element of G with finite order m
    try:
        h2_ok = (g in G) and (int(g.order()) == int(m))
    except Exception:
        h2_ok = False

    # ¬Q: The order of the element (g, h) in the direct product G × H is NOT lcm(m, n)
    try:
        if h not in H:
            # If h is not in H, (g, h) is not in G x H, so the conclusion fails.
            neg_q_ok = True
        else:
            actual_order = math.lcm(int(g.order()), int(h.order()))
            claimed_order = math.lcm(int(m), int(n))
            neg_q_ok = bool(actual_order != claimed_order)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: g is an element of G with finite order m",
    "¬Q: The order of (g, h) in G x H is not lcm(m, n)"
]

N_HYP = 2
NEG_Q_INDEX = 2