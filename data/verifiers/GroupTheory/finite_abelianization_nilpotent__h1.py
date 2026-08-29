import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

class _InfiniteDihedralGroup:
    @property
    def is_finite(self):
        return False
    def abelian_invariants(self):
        return [2, 2]
    def order(self):
        from sympy import oo
        return oo

class _PSL2Z_Group:
    @property
    def is_finite(self):
        return False
    def abelian_invariants(self):
        return [6]
    def order(self):
        from sympy import oo
        return oo

D_infty = _InfiniteDihedralGroup()
PSL2Z = _PSL2Z_Group()

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: The quotient group G/G' is a finite group
    try:
        if hasattr(witness, 'abelian_invariants'):
            invs = witness.abelian_invariants()
            h1 = (0 not in invs)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: G is not a finite group
    try:
        if hasattr(witness, 'is_finite'):
            is_fin = witness.is_finite
            if callable(is_fin):
                neg_q = not is_fin()
            else:
                neg_q = not is_fin
        elif hasattr(witness, 'order'):
            from sympy import oo
            order_val = witness.order() if callable(witness.order) else witness.order
            neg_q = (order_val == oo)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The quotient group G/G' is a finite group",
    "¬Q: G is not a finite group"
]

N_HYP = 1
NEG_Q_INDEX = 1