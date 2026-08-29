import sympy
from sympy import oo
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(grp):
    """Basic check to ensure the object is a group-like SymPy object."""
    if grp is None:
        return False
    if hasattr(grp, 'generators') or hasattr(grp, 'elements') or hasattr(grp, 'order'):
        return True
    return False

def is_virtually_abelian(grp):
    """
    Checks if a group is virtually abelian.
    A group is virtually abelian if it has an abelian subgroup of finite index.
    - All finite groups are virtually abelian.
    - Abelian groups are virtually abelian.
    - Free groups of rank <= 1 are virtually abelian.
    - Free groups of rank > 1 are not virtually abelian.
    """
    if not is_group(grp):
        return False
        
    try:
        if getattr(grp, 'is_abelian', False):
            return True
    except Exception:
        pass

    try:
        if getattr(grp, 'is_finite', False):
            return True
    except Exception:
        pass

    try:
        ord_val = grp.order()
        if ord_val != oo:
            return True
    except Exception:
        pass

    try:
        if type(grp).__name__ == 'FreeGroup':
            return len(grp.generators) <= 1
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    # The witness is expected to provide both G and H, e.g., as a tuple (G, H) or dict.
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: H is a virtually abelian group
    try:
        h1_ok = bool(is_group(H) and is_virtually_abelian(H))
    except Exception:
        h1_ok = False
        
    # ¬Q: The direct product G x H is NOT a virtually abelian group.
    # Fact: G x H is virtually abelian iff BOTH G and H are virtually abelian.
    # Therefore, G x H is NOT virtually abelian iff at least one of them is NOT virtually abelian.
    try:
        g_is_grp = is_group(G)
        h_is_grp = is_group(H)
        g_virt_ab = is_virtually_abelian(G)
        h_virt_ab = is_virtually_abelian(H)
        
        neg_q = bool(g_is_grp and h_is_grp and not (g_virt_ab and h_virt_ab))
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a virtually abelian group",
    "¬Q: The direct product G x H is not a virtually abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1
