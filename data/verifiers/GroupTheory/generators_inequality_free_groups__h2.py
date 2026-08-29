import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        F, S, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: n is a positive integer
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n > 0
    except Exception:
        h1 = False
        
    # H_2: S is a generating set for F
    try:
        if not hasattr(F, 'order'):
            h2 = False
        elif not isinstance(S, (list, tuple, set)):
            h2 = False
        else:
            S_list = list(S)
            all_in_F = True
            for s in S_list:
                if s not in F:
                    all_in_F = False
                    break
            
            if not all_in_F:
                h2 = False
            else:
                if len(S_list) == 0:
                    h2 = (F.order() == 1)
                else:
                    G = PermutationGroup(*S_list)
                    h2 = (G.order() == F.order())
    except Exception:
        h2 = False
        
    # ¬Q: The cardinality of S is strictly less than n
    try:
        neg_q = len(set(S)) < n
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: S is a generating set for F",
    "¬Q: The cardinality of S is strictly less than n"
]

N_HYP = 2
NEG_Q_INDEX = 2