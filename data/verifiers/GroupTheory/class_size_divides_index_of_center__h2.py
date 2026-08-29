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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, x = witness
        else:
            G = witness
            x = None
            
        if not isinstance(G, PermutationGroup):
            h1_ok = False
        else:
            h1_ok = G.is_group and G.order() < float('inf')
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q = False
        else:
            center_order = G.center().order()
            index_center = G.order() // center_order
            
            if x is not None:
                if x not in G.elements:
                    neg_q = False
                else:
                    orbit = set()
                    for g in G.elements:
                        orbit.add(g * x * ~g)
                    class_size = len(orbit)
                    neg_q = (index_center % class_size != 0)
            else:
                neg_q = False
                for element in G.elements:
                    orbit = set()
                    for g in G.elements:
                        orbit.add(g * element * ~g)
                    class_size = len(orbit)
                    if index_center % class_size != 0:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = ["H_1: G is a finite group", "neg_Q: The size of the conjugacy class of x in G does NOT divide the index of the center of G"]
N_HYP = 1
NEG_Q_INDEX = 1