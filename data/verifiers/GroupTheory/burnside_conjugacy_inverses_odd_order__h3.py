import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    # The witness can be either a tuple (G, x) or just the group G.
    # If just G is provided, we check if there exists any x in G that violates the conclusion.
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, x = witness
            x_list = [x]
        else:
            G = witness
            x_list = list(G.generate_elements())
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The order of G is an odd integer
    try:
        h2_ok = bool(G.order() % 2 == 1)
    except Exception:
        h2_ok = False

    # ¬Q: x is conjugate to x^-1 in G
    try:
        neg_q_ok = False
        if h1_ok:
            for x_elem in x_list:
                try:
                    if x_elem not in G:
                        continue
                except Exception:
                    continue
                
                x_inv = ~x_elem
                # Check if x_elem is conjugate to x_inv in G
                for g in G.generate_elements():
                    if g * x_elem * ~g == x_inv:
                        neg_q_ok = True
                        break
                
                if neg_q_ok:
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is an odd integer",
    "¬Q: x is conjugate to x^-1 in G"
]

N_HYP = 2
NEG_Q_INDEX = 2