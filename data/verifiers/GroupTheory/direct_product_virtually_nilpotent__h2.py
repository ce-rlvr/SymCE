import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(g):
    """Check if the object is a recognized group."""
    if isinstance(g, (PermutationGroup, FreeGroup, FpGroup)):
        return True
    if hasattr(g, 'generators') and hasattr(g, 'identity'):
        return True
    return False

def is_virtually_nilpotent(g):
    """
    Check if a group is virtually nilpotent.
    A group is virtually nilpotent if it has a nilpotent subgroup of finite index.
    """
    # All finite groups are virtually nilpotent (the trivial subgroup is nilpotent and has finite index)
    if isinstance(g, PermutationGroup):
        return True
        
    # A free group is virtually nilpotent iff its rank is <= 1
    if isinstance(g, FreeGroup):
        return len(g.generators) <= 1
        
    # For finitely presented groups, check abelian property or if it's a free group of rank <= 1
    if isinstance(g, FpGroup):
        try:
            if callable(g.is_abelian):
                if g.is_abelian():
                    return True
            else:
                if g.is_abelian:
                    return True
        except Exception:
            pass
        if len(g.relators) == 0:
            return len(g.generators) <= 1
            
    # Fallback for any group that explicitly knows it is nilpotent
    try:
        if callable(g.is_nilpotent):
            if g.is_nilpotent():
                return True
        else:
            if g.is_nilpotent:
                return True
    except Exception:
        pass
        
    return False

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H), check the hypotheses and the negated conclusion.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G and H are groups
    try:
        h1_ok = bool(is_group(G) and is_group(H))
    except Exception:
        h1_ok = False
        
    # H_2: H is virtually nilpotent
    try:
        h2_ok = bool(is_virtually_nilpotent(H))
    except Exception:
        h2_ok = False
        
    # ¬Q: G x H is NOT virtually nilpotent
    # The direct product G x H is virtually nilpotent iff BOTH G and H are virtually nilpotent.
    try:
        neg_q_ok = not (is_virtually_nilpotent(G) and is_virtually_nilpotent(H))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: H is virtually nilpotent",
    "¬Q: G x H is not virtually nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2