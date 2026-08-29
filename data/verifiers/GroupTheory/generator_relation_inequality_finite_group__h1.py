import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    """
    The witness is expected to be a tuple (g, r) representing the number of generators
    and the number of relations of a finitely presented group, or a tuple (X, R) 
    representing the list of generators and the list of relations.
    """
    g, r = -1, -1
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int) and isinstance(witness[1], int):
                g, r = witness[0], witness[1]
                h1 = (g >= 0 and r >= 0)
            elif hasattr(witness[0], '__len__') and hasattr(witness[1], '__len__'):
                g = len(witness[0])
                r = len(witness[1])
                h1 = True
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            neg_q = bool(r < g)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G has a finite presentation <X | R>",
    "H_2: g = |X| and r = |R| are well-defined",
    "¬Q: The number of relations r is less than the number of generators g"
]

N_HYP = 2
NEG_Q_INDEX = 2