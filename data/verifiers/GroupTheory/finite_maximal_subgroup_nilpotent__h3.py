import sympy
from sympy import oo, isprime
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard finite groups
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

# Top-level setup for the standard infinite nilpotent group (Z, +)
class Z_group_class:
    def __init__(self):
        self.is_nilpotent = True
        self.is_abelian = True
        self.is_finite = False

    def order(self):
        return oo

    def is_maximal_subgroup(self, M):
        if isinstance(M, nZ_subgroup_class):
            return isprime(M.n)
        return False

class nZ_subgroup_class:
    def __init__(self, n):
        self.n = abs(n)
        self.is_nilpotent = True
        self.is_abelian = True
        self.is_finite = False

    def order(self):
        return oo

Z = Z_group_class()
def nZ(n):
    return nZ_subgroup_class(n)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        G, M = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a nilpotent group
    h1 = False
    try:
        if hasattr(G, 'is_nilpotent'):
            val = G.is_nilpotent
            h1 = bool(val() if callable(val) else val)
        elif hasattr(G, 'is_abelian'):
            val = G.is_abelian
            h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    # H_2: M is a maximal subgroup of G
    h2 = False
    try:
        if hasattr(G, 'is_maximal_subgroup'):
            h2 = bool(G.is_maximal_subgroup(M))
        elif hasattr(G, 'maximal_subgroups'):
            max_subs = G.maximal_subgroups()
            for sub in max_subs:
                try:
                    if sub.is_subgroup(M) and M.is_subgroup(sub):
                        h2 = True
                        break
                except Exception:
                    pass
    except Exception:
        pass

    # neg_Q: G is NOT a finite group
    neg_q = False
    try:
        is_fin = True
        if hasattr(G, 'is_finite'):
            val = G.is_finite
            is_fin = bool(val() if callable(val) else val)
        elif hasattr(G, 'order'):
            val = G.order
            ord_val = val() if callable(val) else val
            if ord_val == oo:
                is_fin = False
            else:
                is_fin = True
        neg_q = not is_fin
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: M is a maximal subgroup of G",
    "¬Q: G is not a finite group"
]

N_HYP = 2
NEG_Q_INDEX = 2