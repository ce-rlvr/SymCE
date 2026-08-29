import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are elements of G",
    "H_3: x and y are conjugate in G",
    "¬Q: x^n and y^n are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_group(G):
    if hasattr(G, 'is_group') and G.is_group:
        return True
    if isinstance(G, PermutationGroup):
        return True
    if hasattr(G, 'elements') and hasattr(G, 'contains'):
        return True
    return False

def in_group(G, x):
    if hasattr(G, 'contains'):
        return G.contains(x)
    if hasattr(G, 'elements'):
        return x in G.elements
    if isinstance(G, (list, tuple, set)):
        return x in G
    return False

def are_conjugate(G, a, b):
    # Fast path for permutations: different cycle structures cannot be conjugate
    if hasattr(a, 'cycle_structure') and hasattr(b, 'cycle_structure'):
        if a.cycle_structure != b.cycle_structure:
            return False
            
    if hasattr(G, 'elements'):
        elements = G.elements
    elif isinstance(G, (list, tuple, set)):
        elements = G
    else:
        return False
        
    for g in elements:
        try:
            if hasattr(g, 'inv'):
                ginv = g.inv()
            else:
                ginv = ~g
            if g * a * ginv == b:
                return True
        except Exception:
            pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            x = witness['x']
            y = witness['y']
            n = witness.get('n', None)
        elif len(witness) == 4:
            G, x, y, n = witness
        elif len(witness) == 3:
            G, x, y = witness
            n = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = is_group(G)
    except Exception:
        h1 = False

    # H2: x and y are elements of G
    try:
        h2 = in_group(G, x) and in_group(G, y)
    except Exception:
        h2 = False

    # H3: x and y are conjugate in G
    try:
        h3 = False
        if h1 and h2:
            h3 = are_conjugate(G, x, y)
    except Exception:
        h3 = False

    # neg_Q: x^n and y^n are NOT conjugate in G
    try:
        neg_q = False
        if h1 and h2:
            if n is not None:
                n_list = [n]
            else:
                # If n is not provided, check if there exists any power n where they are not conjugate
                if hasattr(x, 'order'):
                    if callable(x.order):
                        max_n = x.order()
                    else:
                        max_n = x.order
                else:
                    max_n = 10
                n_list = range(1, max_n + 1)
            
            for n_val in n_list:
                xn = x**n_val
                yn = y**n_val
                if not are_conjugate(G, xn, yn):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]