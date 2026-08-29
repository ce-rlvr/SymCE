import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

CONDITION_LABELS = [
    "H_1: G is a nilpotent group of nilpotency class c",
    "H_2: x is an element of G",
    "¬Q: The c-fold left-normed commutator of x and y is not equal to the identity element of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    G = None
    x = None
    c = None
    y_list = None

    if isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            G, x = witness
        elif len(witness) == 3:
            if isinstance(witness[1], int):
                G, c, x = witness
            else:
                G, x, y = witness
                y_list = [y]
        elif len(witness) == 4:
            G, c, x, y = witness
            y_list = [y]
        else:
            return [False, False, False]
    else:
        return [False, False, False]

    h1 = False
    try:
        if getattr(G, 'is_nilpotent', False):
            actual_c = len(G.lower_central_series()) - 1
            if c is None:
                c = actual_c
                h1 = True
            else:
                h1 = (c == actual_c)
    except Exception:
        h1 = False

    h2 = False
    try:
        if hasattr(G, 'contains'):
            h2 = G.contains(x)
        else:
            h2 = x in G.elements
    except Exception:
        h2 = False

    neg_q = False
    try:
        if c is None:
            if getattr(G, 'is_nilpotent', False):
                c = len(G.lower_central_series()) - 1
            else:
                c = -1
                
        if c >= 1:
            if y_list is None:
                ys = list(G.elements)
            else:
                ys = y_list
                
            try:
                identity = list(G.generators)[0]**-1 * list(G.generators)[0]
            except Exception:
                identity = Permutation()
                    
            for y in ys:
                elements = [x] + [y] * c
                res = elements[0]
                for g in elements[1:]:
                    res = (res**-1) * (g**-1) * res * g
                
                if res != identity:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]