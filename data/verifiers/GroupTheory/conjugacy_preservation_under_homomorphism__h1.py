import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        H = witness['H']
        f = witness['f']
        x = witness['x']
        y = witness['y']
    except Exception:
        return [False, False]

    # H_1: x and y are conjugate elements in G
    h1_ok = False
    try:
        if hasattr(G, 'elements') and x in G.elements and y in G.elements:
            for g in G.elements:
                if g * x * ~g == y or ~g * x * g == y:
                    h1_ok = True
                    break
    except Exception:
        h1_ok = False

    # ¬Q: f(x) and f(y) are not conjugate elements in H
    neg_q_ok = False
    try:
        if callable(f):
            fx = f(x)
            fy = f(y)
        else:
            fx = f[x]
            fy = f[y]
            
        if not hasattr(H, 'elements'):
            neg_q_ok = False
        else:
            conjugate_in_H = False
            if fx in H.elements and fy in H.elements:
                for h in H.elements:
                    if h * fx * ~h == fy or ~h * fx * h == fy:
                        conjugate_in_H = True
                        break
            neg_q_ok = not conjugate_in_H
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x and y are conjugate elements in G",
    "¬Q: f(x) and f(y) are not conjugate elements in H"
]

N_HYP = 1
NEG_Q_INDEX = 1