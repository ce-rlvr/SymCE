import math
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
    # Unpack witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            g = witness.get('g')
            m = witness.get('m')
            h = witness.get('h')
            n = witness.get('n')
        elif hasattr(witness, 'G'):
            G = getattr(witness, 'G', None)
            H = getattr(witness, 'H', None)
            g = getattr(witness, 'g', None)
            m = getattr(witness, 'm', None)
            h = getattr(witness, 'h', None)
            n = getattr(witness, 'n', None)
        else:
            G, H, g, m, h, n = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: h is an element of H with finite order n
    try:
        h2 = bool(h in H and h.order() == n)
    except Exception:
        h2 = False

    # ¬Q: The order of the element (g, h) in the direct product G x H is NOT lcm(m, n)
    try:
        try:
            in_G = bool(g in G)
        except Exception:
            in_G = False
            
        if not in_G:
            # If g is not in G, (g, h) is not in G x H, so the conclusion fails.
            neg_q = True
        else:
            actual_order = sympy.lcm(int(g.order()), int(h.order()))
            expected_order = sympy.lcm(int(m), int(n))
            neg_q = bool(actual_order != expected_order)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: h is an element of H with finite order n",
    "¬Q: The order of (g, h) in G x H is not lcm(m, n)"
]

N_HYP = 2
NEG_Q_INDEX = 2