import sympy
import sympy.combinatorics
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_group(G):
    if G is None:
        return False
    FpGroup = getattr(sympy.combinatorics, 'FpGroup', None)
    FreeGroup = getattr(sympy.combinatorics, 'FreeGroup', None)
    
    valid_classes = [PermutationGroup]
    if FpGroup is not None:
        valid_classes.append(FpGroup)
    if FreeGroup is not None:
        valid_classes.append(FreeGroup)
        
    return isinstance(G, tuple(valid_classes))

def is_derived_subgroup_finite(G):
    if G is None:
        return False
        
    FpGroup = getattr(sympy.combinatorics, 'FpGroup', None)
    FreeGroup = getattr(sympy.combinatorics, 'FreeGroup', None)
    
    if isinstance(G, PermutationGroup):
        return True
    if FreeGroup is not None and isinstance(G, FreeGroup):
        return len(G.generators) <= 1
    if FpGroup is not None and isinstance(G, FpGroup):
        if getattr(G, 'is_abelian', False):
            return True
        # To avoid hanging on infinite FpGroups (e.g., via Todd-Coxeter), 
        # we assume non-abelian FpGroups have infinite derived subgroups.
        return False
    return False

def conditions(witness):
    try:
        if is_group(witness):
            G = witness
        elif isinstance(witness, tuple) and len(witness) >= 1 and is_group(witness[0]):
            G = witness[0]
        else:
            G = witness
    except Exception:
        G = witness

    try:
        h1 = is_group(G)
    except Exception:
        h1 = False

    try:
        # "Let Z(G) be the center of G" is a definitional hypothesis.
        # It holds trivially as long as G is a valid group.
        h2 = h1
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not is_derived_subgroup_finite(G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Z(G) is the center of G",
    "¬Q: The commutator subgroup G' is not a finite group"
]

N_HYP = 2
NEG_Q_INDEX = 2