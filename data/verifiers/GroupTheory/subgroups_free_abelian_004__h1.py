import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # The witness is expected to be a tuple (F, H) or (F, H, n)
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, H, n = witness
            elif len(witness) == 2:
                F, H = witness
                n = None
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: Let H be a subgroup of F
    try:
        h1_ok = bool(H.is_subgroup(F))
    except Exception:
        h1_ok = False

    # ¬Q: H is NOT a free abelian group of rank m, where m <= n
    try:
        from sympy.combinatorics import PermutationGroup
        if isinstance(H, PermutationGroup):
            # A finite group is free abelian if and only if it is the trivial group (order 1, rank 0)
            if H.order() == 1:
                m = 0
                if n is not None:
                    q = (m <= n)
                else:
                    q = True
            else:
                q = False
        else:
            if hasattr(H, 'order'):
                order = H.order()
                if order == 1:
                    m = 0
                    if n is not None:
                        q = (m <= n)
                    else:
                        q = True
                elif order != sympy.oo:
                    # Any finite group of order > 1 is not free abelian
                    q = False
                else:
                    # Cannot reliably determine if an infinite group is free abelian here
                    raise NotImplementedError
            else:
                raise NotImplementedError
                
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of F",
    "¬Q: H is not a free abelian group of rank m with m <= n"
]

N_HYP = 1
NEG_Q_INDEX = 1