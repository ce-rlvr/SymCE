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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = False
        G = None
        
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G_cand, p, k = witness
                if isinstance(G_cand, PermutationGroup):
                    try:
                        if G_cand.order() == p**k and k >= 1:
                            h1 = True
                            G = G_cand
                    except Exception:
                        pass
            elif len(witness) == 2:
                G_cand, p = witness
                if isinstance(G_cand, PermutationGroup):
                    h1 = True
                    G = G_cand
            elif len(witness) == 1:
                G_cand = witness[0]
                if isinstance(G_cand, PermutationGroup):
                    h1 = True
                    G = G_cand
        else:
            G_cand = witness
            if isinstance(G_cand, PermutationGroup):
                h1 = True
                G = G_cand
                
        neg_q = False
        if h1 and G is not None:
            try:
                Z = G.center()
                if Z.order() <= 1:
                    neg_q = True
            except Exception:
                pass
                
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a finite group of order p^k for some integer k >= 1",
    "¬Q: The center of G, Z(G), contains at most one element"
]

N_HYP = 1
NEG_Q_INDEX = 1