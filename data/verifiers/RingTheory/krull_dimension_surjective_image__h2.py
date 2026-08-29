import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z

# Provide some custom ring objects in case the witness uses them instead of SymPy domains
class CustomRing:
    def __init__(self, name, krull_dim):
        self.name = name
        self.is_commutative = True
        self.has_identity = True
        self.krull_dim = krull_dim
        self.is_Field = (krull_dim == 0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

Z_ring = CustomRing("Z", 1)
Q_ring = CustomRing("Q", 0)
Qx_ring = CustomRing("Q[x]", 1)
Qxy_ring = CustomRing("Q[x,y]", 2)

def is_commutative_ring_with_identity(R):
    if hasattr(R, 'is_commutative') and hasattr(R, 'has_identity'):
        if R.is_commutative and R.has_identity:
            return True
    
    if R == QQ or R == ZZ:
        return True
        
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
        
    if hasattr(R, 'domain') and hasattr(R, 'gens'):
        return is_commutative_ring_with_identity(R.domain)
        
    return False

def get_krull_dim(R):
    if hasattr(R, 'krull_dim'):
        return R.krull_dim
    if hasattr(R, 'is_Field') and R.is_Field:
        return 0
    if R == ZZ:
        return 1
    if hasattr(R, 'domain') and hasattr(R, 'gens'):
        return get_krull_dim(R.domain) + len(R.gens)
    raise ValueError(f"Cannot determine Krull dimension of {R}")

def conditions(witness):
    try:
        R, S = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(is_commutative_ring_with_identity(R) and is_commutative_ring_with_identity(S))
    except Exception:
        h1 = False
        
    try:
        dim_R = get_krull_dim(R)
        dim_S = get_krull_dim(S)
        neg_q = bool(dim_S > dim_R)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "¬Q: The Krull dimension of S is strictly greater than the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1