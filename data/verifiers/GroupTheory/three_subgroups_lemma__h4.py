import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def commutator_subgroup(A, B):
    gens = set()
    elements_A = list(A.generate())
    elements_B = list(B.generate())
    for a in elements_A:
        for b in elements_B:
            gens.add(~a * ~b * a * b)
    return PermutationGroup(list(gens))

def is_trivial_group(H):
    try:
        return len(list(H.generate())) == 1
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        G, X, Y, Z = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: X, Y, and Z are subgroups of G
    try:
        def is_subgroup(H, Grp):
            for g in H.generators:
                if g not in Grp:
                    return False
            return True
        
        h2 = (isinstance(X, PermutationGroup) and is_subgroup(X, G) and
              isinstance(Y, PermutationGroup) and is_subgroup(Y, G) and
              isinstance(Z, PermutationGroup) and is_subgroup(Z, G))
    except Exception:
        h2 = False
        
    # H3: The mutual commutator subgroup of X, Y, and Z is the trivial subgroup
    try:
        XY = commutator_subgroup(X, Y)
        XY_Z = commutator_subgroup(XY, Z)
        h3 = is_trivial_group(XY_Z)
    except Exception:
        h3 = False
        
    # neg_Q: The mutual commutator subgroup of Z, X, and Y is not the trivial subgroup
    try:
        ZX = commutator_subgroup(Z, X)
        ZX_Y = commutator_subgroup(ZX, Y)
        neg_q = not is_trivial_group(ZX_Y)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X, Y, and Z are subgroups of G",
    "H_3: The mutual commutator subgroup of X, Y, and Z is the trivial subgroup",
    "not Q: The mutual commutator subgroup of Z, X, and Y is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3