import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: P is a Sylow 2-subgroup of G",
    "¬Q: P is not isomorphic to the dihedral group of order 8"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_order(obj):
    return obj.order() if callable(obj.order) else obj.order

def conditions(witness):
    try:
        # The witness can be a tuple (G, P) or just G (in which case we find P)
        if isinstance(witness, tuple) and len(witness) == 2:
            G, P = witness
        else:
            G = witness
            P = G.sylow_subgroup(2)
    except Exception:
        return [False, False]
        
    # H_1: P is a Sylow 2-subgroup of G
    try:
        g_order = get_order(G)
        p_order = get_order(P)
        
        if g_order == sympy.oo or p_order == sympy.oo:
            h1_ok = False
        else:
            target = 1
            temp = g_order
            while temp > 0 and temp % 2 == 0:
                target *= 2
                temp //= 2
                
            h1_ok = (p_order == target)
            if h1_ok:
                gens = P.generators() if callable(P.generators) else P.generators
                for gen in gens:
                    if gen not in G:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False
        
    # ¬Q: P is not isomorphic to the dihedral group of order 8
    try:
        p_order = get_order(P)
        if p_order != 8:
            is_D8 = False
        else:
            # D8 is the unique group of order 8 with exactly 5 elements of order 2
            elements = list(P.generate())
            order_2_count = sum(1 for g in elements if get_order(g) == 2)
            is_D8 = (order_2_count == 5)
            
        neg_q_ok = not is_D8
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]
