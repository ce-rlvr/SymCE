import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            k = witness['k']
        else:
            G, k = witness
    except Exception:
        return [False, False]

    # H_1: k is the number of distinct conjugacy classes of G
    try:
        if hasattr(G, 'conjugacy_classes'):
            res = G.conjugacy_classes
            classes = list(res() if callable(res) else res)
        elif hasattr(G, 'classes'):
            res = G.classes
            classes = list(res() if callable(res) else res)
        else:
            elements = list(G.elements) if hasattr(G, 'elements') else list(G)
            classes = []
            seen = []
            for x in elements:
                if x in seen:
                    continue
                c = []
                for g in elements:
                    try:
                        inv_g = g**-1
                    except Exception:
                        inv_g = ~g
                    conj = g * x * inv_g
                    if conj not in c:
                        c.append(conj)
                classes.append(c)
                for item in c:
                    if item not in seen:
                        seen.append(item)
        h1_ok = (k == len(classes))
    except Exception:
        h1_ok = False

    # neg_Q: The number of pairs (x, y) in G \times G such that xy = yx is NOT equal to k|G|
    try:
        elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        order_G = len(elements)
        
        commuting_pairs = 0
        for x in elements:
            for y in elements:
                if x * y == y * x:
                    commuting_pairs += 1
                    
        neg_q_ok = bool(commuting_pairs != k * order_G)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k is the number of distinct conjugacy classes of G",
    "¬Q: The number of commuting pairs is not equal to k|G|"
]

N_HYP = 1
NEG_Q_INDEX = 1