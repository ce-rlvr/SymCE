import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
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

def conditions(witness):
    # Parse witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
                def action(g, y): return g(y)
            elif len(witness) == 3:
                G, X, x = witness
                def action(g, y): return g(y)
            elif len(witness) == 4:
                G, X, act, x = witness
                action = act
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group acting on a set X
    try:
        H1 = isinstance(G, PermutationGroup)
    except Exception:
        H1 = False

    # H_2: x is an element of X
    try:
        if hasattr(G, 'degree'):
            H2 = int(x) == x and 0 <= x < G.degree
        else:
            H2 = False
    except Exception:
        H2 = False

    # ¬Q: The pointwise stabilizer of O_x in G is NOT the normal core of G_x in G
    try:
        elements = list(G.generate())
        
        # Orbit of x: O_x = {g.x | g \in G}
        O_x = {action(g, x) for g in elements}
        
        # Pointwise stabilizer of O_x: {h \in G | h.y = y for all y \in O_x}
        pt_stab = set()
        for g in elements:
            if all(action(g, y) == y for y in O_x):
                pt_stab.add(g)
                
        # Stabilizer of x: G_x = {h \in G | h.x = x}
        G_x = {g for g in elements if action(g, x) == x}
        
        # Normal core of G_x: \bigcap_{g \in G} g G_x g^{-1}
        normal_core = set(elements)
        for g in elements:
            g_inv = ~g
            conjugate = {g * h * g_inv for h in G_x}
            normal_core = normal_core.intersection(conjugate)
            
        neg_Q = pt_stab != normal_core
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: x is an element of X",
    "¬Q: The pointwise stabilizer of O_x in G is not the normal core of G_x in G"
]

N_HYP = 2
NEG_Q_INDEX = 2