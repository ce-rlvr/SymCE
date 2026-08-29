import itertools
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_group(X):
    if hasattr(X, 'is_group'):
        return bool(X.is_group)
    if hasattr(sympy.combinatorics, 'PermutationGroup') and isinstance(X, sympy.combinatorics.PermutationGroup):
        return True
    if type(X).__name__ in ('FpGroup', 'FreeGroup'):
        return True
    return False

def is_finitely_generated(X):
    if hasattr(X, 'is_finitely_generated'):
        return bool(X.is_finitely_generated)
    if hasattr(sympy.combinatorics, 'PermutationGroup') and isinstance(X, sympy.combinatorics.PermutationGroup):
        return True
    if type(X).__name__ in ('FpGroup', 'FreeGroup'):
        return True
    if isinstance(X, (set, tuple, list)):
        return True
    if hasattr(X, 'is_finite'):
        return bool(X.is_finite)
    return False

def direct_product(G, H):
    if hasattr(G, 'direct_product'):
        return G.direct_product(H)
    if hasattr(H, 'rdirect_product'):
        return H.rdirect_product(G)
    if isinstance(G, (set, tuple, list)) and not G:
        return []
    if isinstance(H, (set, tuple, list)) and not H:
        return []
    if isinstance(G, (set, tuple, list)) and is_group(H):
        if hasattr(H, 'elements'):
            return list(itertools.product(G, list(H.elements)))
        else:
            class ProductSet:
                def __init__(self, g, h):
                    self.g = g
                    self.h = h
                @property
                def is_finitely_generated(self):
                    return is_finitely_generated(self.g) and is_finitely_generated(self.h)
            return ProductSet(G, H)
    import sympy.combinatorics.group_constructs
    return sympy.combinatorics.group_constructs.DirectProduct(G, H)

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    # H_1: H is a group
    try:
        h1_ok = is_group(H)
    except Exception:
        h1_ok = False
        
    # ¬Q: G x H is finitely generated iff both G and H are finitely generated (must fail)
    try:
        g_fin = is_finitely_generated(G)
        h_fin = is_finitely_generated(H)
        both_fin = g_fin and h_fin
        
        GxH = direct_product(G, H)
        gxh_fin = is_finitely_generated(GxH)
        
        # The conclusion is (gxh_fin == both_fin). We want it to fail.
        neg_q_ok = (gxh_fin != both_fin)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: H is a group",
    "¬Q: Equivalence of finite generation for G x H and G, H fails"
]

N_HYP = 1
NEG_Q_INDEX = 1