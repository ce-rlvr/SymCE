import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    # Extract witness components
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            x = witness['x']
            y = witness['y']
            f = witness['f']
        else:
            G, H, x, y, f = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: x and y are elements of G such that xy = yx
    try:
        h2_ok = (x in G) and (y in G) and (x * y == y * x)
    except Exception:
        h2_ok = False

    # ¬Q: f(x)f(y) != f(y)f(x) in H
    try:
        try:
            fx = f(x)
        except Exception:
            fx = f[x]
            
        try:
            fy = f(y)
        except Exception:
            fy = f[y]
            
        neg_q_ok = (fx in H) and (fy in H) and (fx * fy != fy * fx)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: x and y are elements of G such that xy = yx",
    "¬Q: f(x)f(y) != f(y)f(x) in H"
]

N_HYP = 2
NEG_Q_INDEX = 2