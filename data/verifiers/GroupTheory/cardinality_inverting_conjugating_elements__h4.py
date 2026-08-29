import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard groups
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)  # V4 is isomorphic to a subgroup of A4, but we'll use A4 as a superset if needed
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
    """
    Given a witness (G, x), checks the remaining hypotheses and the negated conclusion.
    The inverting set of x is interpreted as S = { g in G | g * x * g^-1 == x^-1 }.
    (If the alternative definition S = { g in G | x * g * x^-1 == g^-1 } is intended, 
    it is also evaluated to ensure robustness).
    """
    try:
        G, x = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup) and G.is_group and G.order() < float('inf')
    except Exception:
        h1_ok = False

    # H2: x is an element of G
    try:
        h2_ok = x in G.elements
    except Exception:
        h2_ok = False

    # H3: C_G(x) is the centralizer of x in G
    # This is a definitional hypothesis, so it holds by definition if G and x are valid.
    try:
        h3_ok = h1_ok and h2_ok
    except Exception:
        h3_ok = False

    # neg_Q: The cardinality of S is NEITHER 0 NOR |C_G(x)|
    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            elements = list(G.elements)
            x_inv = x**-1
            
            # Centralizer of x in G
            C_G_x = [g for g in elements if g * x == x * g]
            c_order = len(C_G_x)
            
            # Definition 1: S = { g in G | g * x * g^-1 == x^-1 }
            S1 = [g for g in elements if g * x * (g**-1) == x_inv]
            
            # Definition 2: S = { g in G | x * g * x^-1 == g^-1 } (Elements inverted by x)
            S2 = [g for g in elements if x * g * x_inv == g**-1]
            
            # The conclusion fails if the cardinality is neither 0 nor |C_G(x)|.
            # We check both common interpretations of "inverting set" to be safe.
            # If either interpretation makes the conclusion fail, we consider the negation true.
            neg_q_ok = (len(S1) not in (0, c_order)) or (len(S2) not in (0, c_order))
            
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G",
    "H_3: C_G(x) is the centralizer of x in G",
    "¬Q: The cardinality of the inverting set S is neither 0 nor |C_G(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3