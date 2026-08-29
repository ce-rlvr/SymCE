import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup: common rings that might be used as witnesses
ZZ_x = ZZ[x]
QQ_x = QQ[x]
QQ_xy = QQ[x, y]
ZZ_xy = ZZ[x, y]
QQ_xyz = QQ[x, y, z]

def is_field(R):
    return getattr(R, 'is_Field', False)

def krull_dimension(R):
    if getattr(R, 'is_Field', False):
        return 0
    if R.__class__.__name__ == 'IntegerRing' or R == ZZ:
        return 1
    
    # Check for polynomial rings
    if hasattr(R, 'domain') and hasattr(R, 'gens'):
        return krull_dimension(R.domain) + len(R.gens)
    if hasattr(R, 'dom') and hasattr(R, 'gens'):
        return krull_dimension(R.dom) + len(R.gens)
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        return krull_dimension(R.domain) + len(R.symbols)
        
    raise ValueError(f"Cannot determine Krull dimension for {R}")

def conditions(witness) -> list[bool]:
    try:
        # Verify it's a ring-like object to avoid false positives on arbitrary objects
        is_ring = hasattr(witness, 'is_Field') or hasattr(witness, 'domain') or witness == ZZ
        h1 = bool(is_ring and not is_field(witness))
    except Exception:
        h1 = False
        
    try:
        dim = krull_dimension(witness)
        neg_q = bool(dim != 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is not a field",
    "¬Q: The Krull dimension of R is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1