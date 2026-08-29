import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple):
        if len(witness) == 4:
            G, x, g, y = witness
            X = list(range(G.degree)) if hasattr(G, 'degree') else []
            action = lambda perm, pt: perm(pt)
        elif len(witness) == 6:
            G, X, action, x, g, y = witness
        else:
            return [False] * 6
    elif isinstance(witness, dict):
        G = witness.get('G')
        X = witness.get('X', list(range(G.degree)) if hasattr(G, 'degree') else [])
        action = witness.get('action', lambda perm, pt: perm(pt))
        x = witness.get('x')
        g = witness.get('g')
        y = witness.get('y')
    else:
        return [False] * 6

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple, range))
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        h3 = callable(action)
    except Exception:
        h3 = False

    # H4: x \in X
    try:
        h4 = x in X
    except Exception:
        h4 = False

    # H5: g \in G
    try:
        h5 = g in G
    except Exception:
        h5 = False

    # ¬Q: Stab(y) != g Stab(x) g^{-1}
    try:
        is_standard = True
        try:
            if action(g, x) != g(x):
                is_standard = False
        except Exception:
            is_standard = False
            
        if is_standard:
            stab_x = G.stabilizer(x)
            stab_y = G.stabilizer(y)
        else:
            gens_x = []
            gens_y = []
            for perm in G.generate():
                if action(perm, x) == x:
                    gens_x.append(perm)
                if action(perm, y) == y:
                    gens_y.append(perm)
            stab_x = PermutationGroup(gens_x) if gens_x else PermutationGroup([G.identity])
            stab_y = PermutationGroup(gens_y) if gens_y else PermutationGroup([G.identity])
            
        conj_gens = [g * h * g**-1 for h in stab_x.generators]
        if not conj_gens:
            conj_gens = [G.identity]
        conj_stab_x = PermutationGroup(conj_gens)
        
        is_equal = stab_y.is_subgroup(conj_stab_x) and conj_stab_x.is_subgroup(stab_y)
        neg_q = not is_equal
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "H_4: x \\in X",
    "H_5: g \\in G",
    "¬Q: Stab(y) != g Stab(x) g^{-1}"
]

N_HYP = 5
NEG_Q_INDEX = 5