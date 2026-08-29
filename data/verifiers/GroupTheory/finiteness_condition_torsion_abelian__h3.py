import sympy
from sympy import oo
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Standard group theory bindings
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

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: G is finitely generated",
    "¬Q: G is not a finite group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H_1: G is an abelian group
    try:
        h1 = False
        if hasattr(witness, 'is_abelian') and witness.is_abelian is not None:
            val = witness.is_abelian
            h1 = bool(val()) if callable(val) else bool(val)
        else:
            cname = type(witness).__name__
            if cname == 'FreeGroup':
                h1 = len(witness.generators) <= 1
            elif cname == 'PermutationGroup':
                h1 = bool(witness.is_abelian)
            elif cname == 'FpGroup':
                h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    # H_2: G is finitely generated
    try:
        h2 = False
        if hasattr(witness, 'is_finitely_generated') and witness.is_finitely_generated is not None:
            val = witness.is_finitely_generated
            h2 = bool(val()) if callable(val) else bool(val)
        else:
            cname = type(witness).__name__
            if cname in ('FreeGroup', 'FpGroup', 'PermutationGroup'):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: G is not a finite group
    try:
        is_fin = None
        if hasattr(witness, 'is_finite') and witness.is_finite is not None:
            val = witness.is_finite
            is_fin = bool(val()) if callable(val) else bool(val)
        else:
            cname = type(witness).__name__
            if cname == 'PermutationGroup':
                is_fin = True
            elif cname == 'FreeGroup':
                is_fin = len(witness.generators) == 0
            elif cname == 'FpGroup':
                if h1:
                    # For finitely generated abelian groups, 0 in abelian invariants implies an infinite free part
                    invs = witness.abelian_invariants()
                    is_fin = (0 not in invs)
                else:
                    is_fin = (witness.order() < oo)
            elif hasattr(witness, 'order'):
                val = witness.order
                ord_val = val() if callable(val) else val
                is_fin = (ord_val < oo)
        
        if is_fin is None:
            neg_q = False
        else:
            neg_q = not is_fin
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]