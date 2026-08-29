import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup, Permutation
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, P = witness
        else:
            G = witness
            P = G.sylow_subgroup(2)
    except Exception:
        return [False, False]

    # H_1: P is a Sylow 2-subgroup of G
    try:
        is_sub = True
        for g in P.generators:
            if g not in G:
                is_sub = False
                break
        
        if not is_sub:
            h1 = False
        else:
            g_order = G.order()
            p_order = P.order()
            
            k = 0
            temp = g_order
            while temp % 2 == 0 and temp > 0:
                k += 1
                temp //= 2
                
            h1 = (p_order == 2**k)
    except Exception:
        h1 = False

    # neg_Q: P is NOT isomorphic to D_8
    try:
        if P.order() != 8:
            neg_q = True
        else:
            try:
                elems = P.elements
            except AttributeError:
                elems = list(P.generate())
            
            elements_order_2 = sum(1 for g in elems if g.order() == 2)
            # D_8 is the unique group of order 8 with exactly 5 elements of order 2
            is_D8 = (elements_order_2 == 5)
            neg_q = not is_D8
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a Sylow 2-subgroup of G",
    "¬Q: P is not isomorphic to the dihedral group D_8 of order 8"
]

N_HYP = 1
NEG_Q_INDEX = 1
