import sympy
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
O2 = zeros(2,2)
O3 = zeros(3,3)

class _InfiniteCyclicGroup:
    @property
    def is_nilpotent(self):
        return True
    @property
    def is_abelian(self):
        return True
    @property
    def is_finite(self):
        return False
    def order(self):
        return sympy.oo

Z = _InfiniteCyclicGroup()

def check_nilpotent(G):
    try:
        if hasattr(G, 'is_nilpotent'):
            val = G.is_nilpotent
            if callable(val):
                return bool(val())
            elif val is not None:
                return bool(val)
    except Exception:
        pass

    try:
        if hasattr(G, 'is_abelian'):
            val = G.is_abelian
            if callable(val):
                if val(): return True
            elif val is not None:
                if bool(val): return True
    except Exception:
        pass

    return False

def check_finite(G):
    try:
        if hasattr(G, 'is_finite'):
            val = G.is_finite
            if callable(val):
                return bool(val())
            elif val is not None:
                return bool(val)
    except Exception:
        pass

    try:
        if hasattr(G, 'order'):
            val = G.order
            if callable(val):
                return val() < sympy.oo
            elif val is not None:
                return val < sympy.oo
    except Exception:
        pass

    try:
        from sympy.combinatorics import PermutationGroup
        if isinstance(G, PermutationGroup):
            return True
    except Exception:
        pass

    return False

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, M = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(check_nilpotent(G))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(check_finite(M))
    except Exception:
        h2 = False
        
    try:
        neg_q = not bool(check_finite(G))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: M is a finite group",
    "¬Q: G is not a finite group"
]

N_HYP = 2
NEG_Q_INDEX = 2