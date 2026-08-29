import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
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

# Linear algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Provide a standard non-residually finite group: Baumslag-Solitar group BS(2,3)
F_bs, a_bs, b_bs = free_group("a, b")
BS_2_3 = FpGroup(F_bs, [a_bs * b_bs**2 * a_bs**-1 * b_bs**-3])

def is_group(grp):
    return isinstance(grp, (PermutationGroup, FpGroup))

def is_residually_finite(grp):
    """
    Approximates residual finiteness for SymPy group objects.
    Finite groups (PermutationGroup) and Free groups are residually finite.
    Finitely presented groups with relators are assumed not residually finite 
    unless they are trivially abelian, to avoid undecidable word problems and infinite loops.
    """
    if isinstance(grp, PermutationGroup):
        return True
    if isinstance(grp, FpGroup):
        if len(grp.relators) == 0:
            return True
        try:
            if grp.is_abelian:
                return True
        except Exception:
            pass
        return False
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        if not is_group(G) or not is_group(H):
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: H is a residually finite group
    try:
        h1_ok = is_residually_finite(H)
    except Exception:
        h1_ok = False

    # neg_Q: G \times H is NOT a residually finite group
    try:
        # The direct product G x H is residually finite iff both G and H are residually finite.
        # Thus, it is NOT residually finite iff not (is_rf(G) and is_rf(H)).
        neg_q = not (is_residually_finite(G) and is_residually_finite(H))
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a residually finite group",
    "¬Q: G \\times H is not a residually finite group"
]

N_HYP = 1
NEG_Q_INDEX = 1