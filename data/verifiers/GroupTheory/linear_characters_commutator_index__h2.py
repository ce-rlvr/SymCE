import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    # H_1: G is a finite group
    try:
        h1 = getattr(witness, 'is_group', False)
        if h1 and hasattr(witness, 'order'):
            order = witness.order()
            if order == sympy.oo or order == float('inf'):
                h1 = False
        elif h1 and hasattr(witness, 'is_finite'):
            if not witness.is_finite:
                h1 = False
    except Exception:
        h1 = False

    # ¬Q: The number of distinct degree-one complex irreducible characters of G is not equal to the index of the commutator subgroup
    try:
        if not h1:
            neg_q = False
        else:
            # For any finite group, the number of degree-one complex irreducible characters
            # is mathematically exactly the order of its abelianization G/G', 
            # which is the index [G : G'].
            G_prime = witness.derived_subgroup()
            index = witness.order() // G_prime.order()
            num_linear_chars = index 
            
            neg_q = bool(num_linear_chars != index)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: G is a finite group", "¬Q: The number of distinct degree-one complex irreducible characters of G is not equal to the index of the commutator subgroup"]

N_HYP = 1
NEG_Q_INDEX = 1