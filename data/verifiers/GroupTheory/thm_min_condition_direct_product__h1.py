import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

class InfiniteCyclicGroup:
    """A mock class representing the infinite cyclic group Z."""
    @property
    def is_finite(self):
        return False
        
    def order(self):
        from sympy import oo
        return oo

Z_group = InfiniteCyclicGroup()

def is_group(grp):
    if isinstance(grp, InfiniteCyclicGroup):
        return True
    from sympy.combinatorics import PermutationGroup
    if isinstance(grp, PermutationGroup):
        return True
    if hasattr(grp, 'order') and callable(getattr(grp, 'order')):
        return True
    return False

def is_artinian(grp):
    """
    Checks if a group satisfies the minimum condition on subgroups (Artinian).
    For finitely generated groups (which all our available groups are), 
    this is equivalent to being finite.
    """
    if hasattr(grp, 'is_finite'):
        if grp.is_finite is True:
            return True
        if grp.is_finite is False:
            return False
            
    if hasattr(grp, 'order'):
        try:
            from sympy import oo
            ord = grp.order()
            if ord == oo:
                return False
            if ord < oo:
                return True
        except Exception:
            pass
            
    from sympy.combinatorics import PermutationGroup
    if isinstance(grp, PermutationGroup):
        return True
        
    return False

def conditions(witness):
    """
    Given a witness (G, H), checks if it is a counterexample to the conjecture.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
    
    try:
        if not is_group(G) or not is_group(H):
            return [False, False]
    except Exception:
        return [False, False]
    
    # H_1: H satisfies the minimum condition on subgroups
    try:
        h1 = is_artinian(H)
    except Exception:
        h1 = False
        
    # ¬Q: G x H does NOT satisfy the minimum condition on subgroups
    try:
        # The direct product G x H is Artinian iff both G and H are Artinian.
        g_art = is_artinian(G)
        h_art = is_artinian(H)
        q = g_art and h_art
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H satisfies the minimum condition on subgroups",
    "¬Q: G x H does not satisfy the minimum condition on subgroups"
]

N_HYP = 1
NEG_Q_INDEX = 1
