import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        F, A = witness
    except Exception:
        return [False, False]
    
    # H_1: A is a non-trivial maximal abelian subgroup of F
    try:
        h1 = False
        if hasattr(A, 'generators') and hasattr(F, 'generators'):
            A_gens = A.generators() if callable(A.generators) else A.generators
            # Check if A is a subgroup of F
            if all(g in F for g in A_gens):
                order_A = A.order() if callable(A.order) else A.order
                is_ab = A.is_abelian() if callable(A.is_abelian) else A.is_abelian
                if order_A > 1 and is_ab:
                    is_max = True
                    order_F = F.order() if callable(F.order) else F.order
                    if order_F < float('inf') and order_F != sympy.oo:
                        try:
                            elements = F.elements
                        except AttributeError:
                            elements = list(F.generate())
                        
                        for g in elements:
                            if g not in A:
                                if all(g * a == a * g for a in A_gens):
                                    is_max = False
                                    break
                        h1 = is_max
    except Exception:
        h1 = False

    # neg_Q: A is not an infinite cyclic group
    try:
        is_inf_cyclic = False
        if hasattr(A, 'order'):
            order_A = A.order() if callable(A.order) else A.order
            if order_A == float('inf') or order_A == sympy.oo:
                is_inf_cyclic = True
        neg_q = not is_inf_cyclic
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a non-trivial maximal abelian subgroup of F",
    "¬Q: A is not an infinite cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1