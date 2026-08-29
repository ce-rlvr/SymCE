import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def is_group(obj):
    """Check if the object represents a group."""
    if hasattr(obj, 'is_group'):
        return obj.is_group
    if isinstance(obj, (PermutationGroup, FpGroup, FreeGroup)):
        return True
    if hasattr(obj, 'identity') and hasattr(obj, 'elements'):
        return True
    return False

def is_finitely_generated(obj):
    """Check if the object is finitely generated."""
    if hasattr(obj, 'is_finitely_generated'):
        return obj.is_finitely_generated
    if isinstance(obj, (PermutationGroup, FpGroup, FreeGroup)):
        return True
    if hasattr(obj, 'generators'):
        try:
            if hasattr(obj.generators, '__len__'):
                return True
        except Exception:
            pass
    return False

def get_direct_product(G, H):
    """Compute the direct product of G and H."""
    if hasattr(G, 'direct_product'):
        return G.direct_product(H)
    if hasattr(G, '__mul__'):
        return G * H
    raise ValueError("Cannot compute direct product")

def conditions(witness) -> list[bool]:
    """
    Evaluate the remaining hypotheses and the negated conclusion at the witness.
    The witness should provide the objects G and H.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        elif isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
        else:
            G = witness.G
            H = witness.H
    except Exception:
        return [False, False]
        
    # H_1: G is a group
    try:
        h1 = bool(is_group(G))
    except Exception:
        h1 = False
        
    # ¬Q: G x H is finitely generated if and only if both G and H are finitely generated is FALSE
    try:
        g_fin = bool(is_finitely_generated(G))
        h_fin = bool(is_finitely_generated(H))
        
        GH = get_direct_product(G, H)
        gh_fin = bool(is_finitely_generated(GH))
        
        # The conclusion is the biconditional
        q = (gh_fin == (g_fin and h_fin))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The equivalence (G x H is finitely generated iff both G and H are finitely generated) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1