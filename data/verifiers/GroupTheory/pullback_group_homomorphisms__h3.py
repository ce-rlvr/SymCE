import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness):
    try:
        G1, G2, H, f1, f2 = witness
    except Exception:
        return [False, False, False]
    
    def eval_f(f, x):
        if isinstance(f, dict):
            return f[x]
        return f(x)

    # H_1: G_1, G_2, and H are groups
    try:
        h1 = (hasattr(G1, 'elements') and hasattr(G1, 'identity') and
              hasattr(G2, 'elements') and hasattr(G2, 'identity') and
              hasattr(H, 'elements') and hasattr(H, 'identity'))
    except Exception:
        h1 = False

    # H_2: f_1: G_1 -> H is a group homomorphism
    try:
        h2 = True
        if h1:
            H_elems = set(H.elements)
            for x in G1.elements:
                fx = eval_f(f1, x)
                if fx not in H_elems:
                    h2 = False
                    break
                for y in G1.elements:
                    fy = eval_f(f1, y)
                    fxy = eval_f(f1, x * y)
                    if fxy != fx * fy:
                        h2 = False
                        break
                if not h2:
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The set {(x, y) in G_1 x G_2 | f_1(x) = f_2(y)} is not a subgroup of G_1 x G_2
    try:
        neg_q = False
        if h1:
            P = set()
            for x in G1.elements:
                fx = eval_f(f1, x)
                for y in G2.elements:
                    fy = eval_f(f2, y)
                    if fx == fy:
                        P.add((x, y))
            
            if not P:
                neg_q = True
            else:
                id1 = G1.identity
                id2 = G2.identity
                if (id1, id2) not in P:
                    neg_q = True
                else:
                    # Check closure
                    for (x1, y1) in P:
                        for (x2, y2) in P:
                            if (x1 * x2, y1 * y2) not in P:
                                neg_q = True
                                break
                        if neg_q:
                            break
                    if not neg_q:
                        # Check inverses
                        for (x, y) in P:
                            if (x**-1, y**-1) not in P:
                                neg_q = True
                                break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G_1, G_2, and H are groups",
    "H_2: f_1: G_1 -> H is a group homomorphism",
    "¬Q: The set {(x, y) in G_1 x G_2 | f_1(x) = f_2(y)} is not a subgroup of G_1 x G_2"
]

N_HYP = 2
NEG_Q_INDEX = 2