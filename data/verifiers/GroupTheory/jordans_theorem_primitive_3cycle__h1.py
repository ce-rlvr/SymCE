import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: G is a primitive permutation group acting on a finite set X of size n
    try:
        h1 = False
        if isinstance(witness, PermutationGroup):
            h1 = bool(witness.is_primitive())
    except Exception:
        h1 = False

    # H_2: G contains a 3-cycle
    try:
        h2 = False
        if isinstance(witness, PermutationGroup):
            n = witness.degree
            if n >= 3:
                order = witness.order()
                fact_n = math.factorial(n)
                if order == fact_n or order == fact_n // 2:
                    h2 = True
                else:
                    count = 0
                    iterator = witness.generate() if hasattr(witness, 'generate') else witness.elements
                    for g in iterator:
                        if g.order() == 3 and len(g.support()) == 3:
                            h2 = True
                            break
                        count += 1
                        if count > 5000:
                            break
    except Exception:
        h2 = False

    # ¬Q: G is neither the alternating group A_n nor the symmetric group S_n
    try:
        neg_q = False
        if isinstance(witness, PermutationGroup):
            n = witness.degree
            order = witness.order()
            fact_n = math.factorial(n)
            is_Sn = (order == fact_n)
            is_An = (order == fact_n // 2)
            neg_q = not (is_Sn or is_An)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a primitive permutation group acting on a finite set X of size n",
    "H_2: G contains a 3-cycle",
    "¬Q: G is neither the alternating group A_n nor the symmetric group S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2