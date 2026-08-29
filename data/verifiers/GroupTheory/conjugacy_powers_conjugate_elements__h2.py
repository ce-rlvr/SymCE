import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    try:
        G, x, y, n = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: x and y are conjugate in G
    try:
        h2 = False
        if h1:
            elems = list(G.elements)
            if x in elems and y in elems:
                for g in elems:
                    if g * x * ~g == y or ~g * x * g == y:
                        h2 = True
                        break
    except Exception:
        h2 = False
        
    # H_3: n is an integer
    try:
        h3 = isinstance(n, int)
    except Exception:
        h3 = False
        
    # ¬Q: x^n and y^n are not conjugate in G
    try:
        neg_q = False
        if h1 and h3:
            elems = list(G.elements)
            if x in elems and y in elems:
                xn = x ** n
                yn = y ** n
                are_conj = False
                for g in elems:
                    if g * xn * ~g == yn or ~g * xn * g == yn:
                        are_conj = True
                        break
                neg_q = not are_conj
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are conjugate in G",
    "H_3: n is an integer",
    "¬Q: x^n and y^n are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3