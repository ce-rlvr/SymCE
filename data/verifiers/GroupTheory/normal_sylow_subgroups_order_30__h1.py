import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # Check H_1: The order of G is 30
    try:
        order_ok = bool(witness.order() == 30)
    except Exception:
        order_ok = False

    # Check ¬Q: G does NOT have both a unique normal Sylow 3-subgroup and a unique normal Sylow 5-subgroup
    try:
        count_3 = 0
        count_5 = 0
        
        # Count elements of order 3 and 5
        for g in witness.generate():
            if g.order() == 3:
                count_3 += 1
            elif g.order() == 5:
                count_5 += 1
                
        # A Sylow p-subgroup is unique (and thus normal) iff n_p = 1.
        # If n_3 = 1, there is exactly 1 subgroup of order 3, which contains exactly 2 elements of order 3.
        # If n_5 = 1, there is exactly 1 subgroup of order 5, which contains exactly 4 elements of order 5.
        n3_is_1 = (count_3 == 2)
        n5_is_1 = (count_5 == 4)
        
        # The conclusion is that BOTH are unique and normal
        conclusion = n3_is_1 and n5_is_1
        
        # We want the negation of the conclusion
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [order_ok, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is 30",
    "¬Q: G does not have both a unique normal Sylow 3-subgroup and a unique normal Sylow 5-subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1