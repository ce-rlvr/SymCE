import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def is_virtually_nilpotent(G):
    """
    A group is virtually nilpotent if it has a nilpotent subgroup of finite index.
    Since all PermutationGroups in SymPy are finite, the trivial subgroup is always
    nilpotent and of finite index. Thus, all finite groups are virtually nilpotent.
    """
    if isinstance(G, PermutationGroup):
        return True
    
    # Fallback for other potential group types
    if hasattr(G, 'is_nilpotent'):
        if callable(G.is_nilpotent):
            try:
                if G.is_nilpotent():
                    return True
            except Exception:
                pass
        else:
            if G.is_nilpotent:
                return True
    return False

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1_ok = is_virtually_nilpotent(G)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = is_virtually_nilpotent(H)
    except Exception:
        h2_ok = False
        
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            # In SymPy, the multiplication operator on PermutationGroups gives the direct product
            GxH = G * H
            q = is_virtually_nilpotent(GxH)
        else:
            # If we cannot compute the direct product, we cannot verify the negated conclusion
            q = True
    except Exception:
        q = True
        
    neg_q_ok = not q
    
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is virtually nilpotent",
    "H_2: H is virtually nilpotent",
    "¬Q: G x H is not virtually nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2