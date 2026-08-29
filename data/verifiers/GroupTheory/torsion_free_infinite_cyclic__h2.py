import sympy
from sympy import S, ZZ
from sympy.combinatorics.free_groups import FreeGroup

# Top-level setup
Z = S.Integers
F1 = FreeGroup('a')

CONDITION_LABELS = [
    "H_1: G is an infinite cyclic group",
    "H_2: x is an element of G",
    "H_3: There exists a non-zero integer k such that x^k = e",
    "¬Q: x is not equal to the identity element e"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_identity(G):
    if G is S.Integers or G is ZZ:
        return 0
    if hasattr(G, 'identity'):
        return G.identity
    return None

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, x, k = witness
            elif len(witness) == 2:
                G, x = witness
                k = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is an infinite cyclic group
    try:
        h1 = False
        if G is S.Integers or G is ZZ:
            h1 = True
        elif isinstance(G, FreeGroup) and len(G.generators) == 1:
            h1 = True
        elif getattr(G, 'is_cyclic', False) and getattr(G, 'is_infinite', False):
            h1 = True
    except Exception:
        h1 = False

    # H2: x is an element of G
    try:
        h2 = False
        if G is S.Integers or G is ZZ:
            if x in S.Integers:
                h2 = True
        else:
            if x in G:
                h2 = True
    except Exception:
        h2 = False

    # H3: There exists a non-zero integer k such that x^k = e
    try:
        h3 = False
        if k is not None:
            k_int = int(k)
            if k_int != 0 and k == k_int:
                if G is S.Integers or G is ZZ:
                    if k_int * x == 0:
                        h3 = True
                else:
                    if x**k_int == get_identity(G):
                        h3 = True
        else:
            if x == get_identity(G):
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: x is not equal to the identity element e
    try:
        neg_q = False
        ident = get_identity(G)
        if ident is not None:
            if bool(x != ident):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]