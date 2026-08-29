import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are elements of G",
    "H_3: x^2 = e and y^2 = e",
    "¬Q: g is not conjugate to its inverse in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Extract witness components
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            y = witness.get('y')
            if 'g' in witness:
                g = witness['g']
            else:
                g = x * y
        else:
            if len(witness) == 3:
                G, x, y = witness
                g = x * y
            else:
                G, x, y, g = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = hasattr(G, 'identity') and hasattr(G, 'elements')
    except Exception:
        h1 = False

    # H_2: x and y are elements of G
    try:
        h2 = bool(x in G and y in G)
    except Exception:
        h2 = False

    # H_3: x^2 = e and y^2 = e
    try:
        e = G.identity
        h3 = bool(x**2 == e and y**2 == e)
    except Exception:
        h3 = False

    # ¬Q: g is not conjugate to its inverse in G
    try:
        if g not in G:
            neg_q = False
        else:
            g_inv = g**-1
            is_conj = False
            # Check if there exists h in G such that h * g * h^-1 == g^-1
            for h in G.elements:
                if h * g * (h**-1) == g_inv:
                    is_conj = True
                    break
            neg_q = not is_conj
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]