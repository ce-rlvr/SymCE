import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def _has_max_condition(grp):
    if hasattr(grp, 'has_max_condition'):
        val = grp.has_max_condition
        return val() if callable(val) else bool(val)
    
    try:
        if grp.order() != sympy.oo:
            return True
    except Exception:
        pass
        
    try:
        from sympy.combinatorics.free_groups import FreeGroup
        if isinstance(grp, FreeGroup):
            return len(grp.generators) <= 1
    except Exception:
        pass
        
    return False

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    try:
        h1_ok = bool(_has_max_condition(G))
    except Exception:
        h1_ok = False
        
    try:
        try:
            from sympy.combinatorics.group_constructs import DirectProduct
            GxH = DirectProduct(G, H)
            q_ok = _has_max_condition(GxH)
        except Exception:
            q_ok = _has_max_condition(G) and _has_max_condition(H)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G satisfies the maximum condition on subgroups",
    "¬Q: The direct product G x H does not satisfy the maximum condition on subgroups"
]

N_HYP = 1
NEG_Q_INDEX = 1