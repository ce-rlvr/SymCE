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
    # Extract witness components
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
            x = witness.get('x')
            y = witness.get('y')
        else:
            G, H, f, x, y = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G and H are groups (and x, y are elements of G)
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)):
            h1 = False
        else:
            G_elems = list(G.elements)
            h1 = (x in G_elems) and (y in G_elems)
    except Exception:
        h1 = False

    # H_2: f: G -> H is a group homomorphism
    try:
        G_elems = list(G.elements)
        H_elems = list(H.elements)
        if callable(f):
            h2 = all(f(a) in H_elems for a in G_elems) and \
                 all(f(a * b) == f(a) * f(b) for a in G_elems for b in G_elems)
        else:
            h2 = all(a in f for a in G_elems) and \
                 all(f[a] in H_elems for a in G_elems) and \
                 all(f[a * b] == f[a] * f[b] for a in G_elems for b in G_elems)
    except Exception:
        h2 = False

    # H_3: H is an abelian group
    try:
        h3 = bool(H.is_abelian)
    except Exception:
        h3 = False

    # ¬Q: f(x) != f(y)
    try:
        if callable(f):
            neg_q = bool(f(x) != f(y))
        else:
            neg_q = bool(f[x] != f[y])
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G -> H is a group homomorphism",
    "H_3: H is an abelian group",
    "¬Q: f(x) != f(y)"
]

N_HYP = 3
NEG_Q_INDEX = 3