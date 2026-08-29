import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.free_groups import FreeGroup, free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import oo, nan, eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_free_group_of_finite_rank(F):
    if isinstance(F, FreeGroup):
        return True, len(F.generators)
    try:
        if hasattr(F, 'order'):
            o = F.order() if callable(F.order) else F.order
            if o == 1:
                return True, 0
    except Exception:
        pass
    return False, None

def is_group(G):
    if isinstance(G, (PermutationGroup, FreeGroup)):
        return True
    if hasattr(G, 'is_group') and G.is_group:
        return True
    return False

def get_order(G):
    if isinstance(G, FreeGroup):
        if len(G.generators) == 0:
            return 1
        return oo
    try:
        if hasattr(G, 'order'):
            o = G.order() if callable(G.order) else G.order
            return o
        if hasattr(G, '__len__'):
            return len(G)
    except Exception:
        pass
    return None

def is_nan(x):
    if x is nan:
        return True
    if hasattr(x, 'has') and x.has(nan):
        return True
    if x != x:
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        F, G = witness
    except Exception:
        return [False, False]

    # H1: F is a free group of finite rank n
    try:
        is_free, n = is_free_group_of_finite_rank(F)
        h1 = bool(is_free)
    except Exception:
        h1 = False

    # neg_Q: The number of distinct group homomorphisms from F to G is NOT exactly |G|^n
    try:
        if not h1:
            neg_q = False
        else:
            order_G = get_order(G)
            if order_G is None:
                neg_q = False
            else:
                expected = order_G ** n
                
                if is_group(G):
                    if order_G == oo:
                        if n == 0:
                            num_hom = 1
                        else:
                            num_hom = oo
                    else:
                        num_hom = order_G ** n
                else:
                    num_hom = 0
                    
                if is_nan(expected):
                    conclusion_holds = False
                else:
                    conclusion_holds = (num_hom == expected)
                    
                neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group of finite rank n",
    "¬Q: The number of distinct group homomorphisms from F to G is NOT exactly |G|^n"
]

N_HYP = 1
NEG_Q_INDEX = 1