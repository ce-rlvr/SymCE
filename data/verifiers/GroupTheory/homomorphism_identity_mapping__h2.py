import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_identity(group):
    if hasattr(group, 'identity'):
        return group.identity
    if hasattr(group, 'generate'):
        for g in group.generate():
            if g * g == g:
                return g
    if hasattr(group, 'elements'):
        for g in group.elements:
            if g * g == g:
                return g
    return None

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False]
        G, H, f = witness
    except Exception:
        return [False, False]

    # H_1: G and H are groups with identities e_G and e_H respectively
    try:
        h1_G = isinstance(G, PermutationGroup) or hasattr(G, 'identity') or hasattr(G, 'generate')
        h1_H = isinstance(H, PermutationGroup) or hasattr(H, 'identity') or hasattr(H, 'generate')
        h1 = bool(h1_G and h1_H)
    except Exception:
        h1 = False

    # ¬Q: f(e_G) != e_H
    try:
        e_G = get_identity(G)
        e_H = get_identity(H)
        
        if e_G is None or e_H is None:
            neg_q = False
        else:
            if callable(f):
                val = f(e_G)
            elif isinstance(f, dict):
                val = f[e_G]
            else:
                val = next(v for k, v in f if k == e_G)
            
            neg_q = bool(val != e_H)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups with identities e_G and e_H respectively",
    "¬Q: f(e_G) != e_H"
]

N_HYP = 1
NEG_Q_INDEX = 1