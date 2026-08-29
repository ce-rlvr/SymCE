import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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

def conditions(witness):
    try:
        # H_1: G is a finite abelian group
        if not witness.is_abelian:
            return [False, False]
        if witness.order() > 2000:
            return [False, False]
        h1_ok = True
    except Exception:
        return [False, False]

    try:
        elements = list(witness.elements)
        order = len(elements)
        
        exp = 1
        for g in elements:
            o = g.order()
            exp = (exp * o) // math.gcd(exp, o)
            
        # P: U(Z[G]) is finite
        # By Higman's Theorem, for a finite abelian group G, 
        # U(Z[G]) is finite iff the exponent of G divides 4 or 6.
        P = exp in [1, 2, 3, 4, 6]
        
        # Q: G is an elementary abelian 2-group, or a cyclic group of order 1, 2, 3, 4, or 6
        is_elem_2 = (exp in [1, 2])
        
        is_cyclic = False
        for g in elements:
            if g.order() == order:
                is_cyclic = True
                break
                
        is_cyclic_12346 = is_cyclic and (order in [1, 2, 3, 4, 6])
        
        Q = is_elem_2 or is_cyclic_12346
        
        # The conclusion is P <-> Q. It fails if P != Q.
        neg_q_ok = bool(P != Q)
        
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: G is a finite abelian group", "not Q: conclusion fails"]
N_HYP = 1
NEG_Q_INDEX = 1