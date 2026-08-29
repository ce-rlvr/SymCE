import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to provide F, G, and pi. Since SymPy does not natively
    support infinitely presented groups, the witness may be a mock object or a dictionary
    with the appropriate boolean flags/methods.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            F, G, pi = witness
        elif isinstance(witness, dict):
            F = witness.get('F')
            G = witness.get('G')
            pi = witness.get('pi')
        else:
            F = witness.F
            G = witness.G
            pi = witness.pi
    except Exception:
        return [False, False, False]

    # H_1: F is a finitely generated free group.
    h1 = False
    try:
        is_free = getattr(F, 'is_FreeGroup', None)
        if callable(is_free): is_free = is_free()
        if is_free is None:
            is_free = type(F).__name__ == 'FreeGroup'

        is_fg = getattr(F, 'is_finitely_generated', None)
        if callable(is_fg): is_fg = is_fg()
        if is_fg is None:
            if type(F).__name__ == 'FreeGroup':
                is_fg = hasattr(F, 'rank') and F.rank < float('inf')

        if is_free and is_fg:
            h1 = True
    except Exception:
        pass

    # H_2: pi is a surjective group homomorphism from F to G.
    h2 = False
    try:
        domain = getattr(pi, 'domain', None)
        codomain = getattr(pi, 'codomain', None)
        if domain is not None and codomain is not None and domain == F and codomain == G:
            is_hom = getattr(pi, 'is_GroupHomomorphism', None)
            if callable(is_hom): is_hom = is_hom()
            if is_hom is None:
                is_hom = type(pi).__name__ == 'GroupHomomorphism'
                
            is_surj = getattr(pi, 'is_surjective', None)
            if callable(is_surj): is_surj = is_surj()
            
            if is_hom and is_surj:
                h2 = True
    except Exception:
        pass

    # ¬Q: The kernel of pi is NOT the normal closure of a finite subset of F.
    # This is mathematically equivalent to G NOT being finitely presented.
    neg_q = False
    try:
        ker_fg = getattr(pi, 'kernel_is_fg_normal', None)
        if callable(ker_fg): ker_fg = ker_fg()
        
        if ker_fg is False:
            neg_q = True
        elif ker_fg is True:
            neg_q = False
        else:
            is_fp = getattr(G, 'is_finitely_presented', None)
            if callable(is_fp): is_fp = is_fp()
            
            if is_fp is False:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finitely generated free group",
    "H_2: pi is a surjective group homomorphism from F to G",
    "¬Q: The kernel of pi is not the normal closure of a finite subset of F"
]

N_HYP = 2
NEG_Q_INDEX = 2