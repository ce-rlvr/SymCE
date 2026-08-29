import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_num_conjugacy_classes(G):
    try:
        cc = G.conjugacy_classes
        if callable(cc):
            return len(cc())
        else:
            return len(cc)
    except Exception:
        pass
    
    elements = list(G.elements)
    classes = []
    unseen = set(elements)
    while unseen:
        x = unseen.pop()
        c = set()
        for g in elements:
            c.add(g * x * (g**-1))
        classes.append(c)
        unseen -= c
    return len(classes)

def conditions(witness):
    G, k, r = None, None, None
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            k = witness.get('k')
            r = witness.get('r')
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, k, r = witness
        else:
            G = witness
            k = get_num_conjugacy_classes(G)
            r = k + 1
    except Exception:
        pass

    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    try:
        actual_k = get_num_conjugacy_classes(G)
        h2 = (k == actual_k)
    except Exception:
        h2 = False

    try:
        neg_q = (k != r)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: k is the number of conjugacy classes of G",
    "¬Q: k != r"
]

N_HYP = 2
NEG_Q_INDEX = 2