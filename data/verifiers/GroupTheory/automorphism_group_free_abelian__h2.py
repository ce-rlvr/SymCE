import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    "H_1: n is a positive integer",
    "¬Q: The automorphism group of G is not isomorphic to GL(n, Z)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        G, n = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and bool(n > 0)
    except Exception:
        h1 = False
        
    try:
        if not hasattr(G, 'order'):
            # If G is not a finite group (e.g., it's symbolic or infinite),
            # we cannot easily compute its automorphism group.
            neg_q = False
        else:
            if n >= 2:
                # GL(n, Z) is infinite for n >= 2.
                # Since G is a finite group, Aut(G) is finite.
                # A finite group cannot be isomorphic to an infinite group.
                neg_q = True
            elif n == 1:
                # GL(1, Z) is isomorphic to Z/2Z (order 2).
                # Aut(G) is isomorphic to Z/2Z iff |Aut(G)| == 2.
                # For finite groups, |Aut(G)| == 2 iff G is isomorphic to Z3, Z4, or Z6.
                o = G.order()
                if o == 3:
                    neg_q = False
                elif o == 4:
                    if any(g.order() == 4 for g in G.elements):
                        neg_q = False
                    else:
                        neg_q = True
                elif o == 6:
                    if G.is_abelian:
                        neg_q = False
                    else:
                        neg_q = True
                else:
                    neg_q = True
            else:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]