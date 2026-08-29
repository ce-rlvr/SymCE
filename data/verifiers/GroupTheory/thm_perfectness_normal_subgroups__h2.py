import sympy
from sympy.combinatorics import PermutationGroup, AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    H1 = False
    neg_Q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, N = witness
        else:
            return [False, False]
            
        def get_order(grp):
            o = grp.order
            return o() if callable(o) else o

        def get_is_solvable(grp):
            s = grp.is_solvable
            return s() if callable(s) else s

        if hasattr(G, 'order') and hasattr(G, 'normal_subgroups'):
            g_ord = get_order(G)
            if g_ord >= 1:
                has_solvable_normal = False
                for ns in G.normal_subgroups():
                    if get_order(ns) > 1 and get_is_solvable(ns):
                        has_solvable_normal = True
                        break
                if not has_solvable_normal:
                    H1 = True
                    
        if hasattr(N, 'derived_subgroup') and hasattr(N, 'order'):
            n_ord = get_order(N)
            der_n = N.derived_subgroup()
            if get_order(der_n) != n_ord:
                neg_Q = True
                
    except Exception:
        pass

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "¬Q: The derived subgroup of N is not equal to N"
]

N_HYP = 1
NEG_Q_INDEX = 1