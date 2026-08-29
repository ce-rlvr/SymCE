import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.group_constructs import DirectProduct
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
V4 = DirectProduct(CyclicGroup(2), CyclicGroup(2))
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_field(F):
    if isinstance(F, str) and F in ['C', 'R', 'Q', 'CC', 'RR', 'QQ', 'Complexes', 'Reals', 'Rationals']:
        return True
    try:
        if hasattr(F, 'is_Field') and F.is_Field:
            return True
    except Exception:
        pass
    try:
        from sympy.polys.domains import Field
        if isinstance(F, Field):
            return True
    except Exception:
        pass
    return False

def embeds_in_GL(grp, k, F):
    if not hasattr(grp, 'order'):
        return False
    try:
        if k < 0:
            return False
        if grp.order() == 1:
            return True
            
        is_C = False
        if isinstance(F, str) and F in ['C', 'CC', 'Complexes']:
            is_C = True
            
        if is_C and getattr(grp, 'is_abelian', False):
            try:
                invs = grp.abelian_invariants()
                return len(invs) <= k
            except Exception:
                pass
                
        if hasattr(grp, 'degree') and k >= grp.degree:
            return True
        if k >= grp.order():
            return True
            
        try:
            if k >= 2 and grp.is_isomorphic(SymmetricGroup(3)):
                return True
            if k >= 1 and grp.is_isomorphic(CyclicGroup(2)):
                return True
        except Exception:
            pass
    except Exception:
        pass
        
    return False

def does_not_embed_in_GL(grp, k, F):
    if not hasattr(grp, 'order'):
        return True
    try:
        if k < 0:
            return True
        if k == 0 and grp.order() > 1:
            return True
            
        is_char_0 = False
        if isinstance(F, str) and F in ['C', 'CC', 'R', 'RR', 'Q', 'QQ', 'Complexes', 'Reals', 'Rationals']:
            is_char_0 = True
        else:
            try:
                if F.char == 0:
                    is_char_0 = True
            except Exception:
                pass
                
        if is_char_0 and getattr(grp, 'is_abelian', False):
            try:
                invs = grp.abelian_invariants()
                return len(invs) > k
            except Exception:
                pass
    except Exception:
        pass
        
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            F = witness.get('F')
            n = int(witness.get('n', -1))
            m = int(witness.get('m', -1))
        elif isinstance(witness, (list, tuple)) and len(witness) == 5:
            G, H, F, n, m = witness
            n = int(n)
            m = int(m)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1 = is_field(F)
    except Exception:
        h1 = False
        
    # H_2: H is a group isomorphic to a subgroup of GL_m(F)
    try:
        h2 = embeds_in_GL(H, m, F)
    except Exception:
        h2 = False
        
    # neg_Q: G x H is NOT isomorphic to a subgroup of GL_{n+m}(F)
    try:
        GxH = DirectProduct(G, H)
        neg_q = does_not_embed_in_GL(GxH, n + m, F)
    except Exception:
        # If DirectProduct fails, GxH is not a valid group, so it cannot be isomorphic to a subgroup
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: H is a group isomorphic to a subgroup of GL_m(F)",
    "¬Q: G \\times H is not isomorphic to a subgroup of GL_{n+m}(F)"
]

N_HYP = 2
NEG_Q_INDEX = 2