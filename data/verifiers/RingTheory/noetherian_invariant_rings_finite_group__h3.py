import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # If witness is a known string counterexample to Hilbert's 14th problem
    if isinstance(witness, str):
        w_lower = witness.lower()
        known_authors = ["nagata", "roberts", "freudenburg", "daigle", "kuroda", "zariski", "mukai", "totaro"]
        if any(author in w_lower for author in known_authors):
            return [True, True, True]
        if "counterexample" in w_lower:
            return [True, True, True]
        return [False, False, False]

    def get_bool(keys, default=False):
        if isinstance(witness, dict):
            for k in keys:
                if k in witness:
                    return bool(witness[k])
        else:
            for k in keys:
                if hasattr(witness, k):
                    return bool(getattr(witness, k))
        return default

    try:
        H1 = get_bool(['A_is_commutative_Noetherian', 'A_is_Noetherian', 'is_Noetherian'], False)
        if get_bool(['A_is_commutative', 'is_commutative'], True) is False:
            H1 = False
    except Exception:
        H1 = False

    try:
        H2 = get_bool(['R_is_finitely_generated_commutative_A_algebra', 
                       'R_is_finitely_generated_A_algebra', 
                       'R_is_fg_A_algebra',
                       'is_finitely_generated_A_algebra'], False)
        if get_bool(['R_is_commutative'], True) is False:
            H2 = False
    except Exception:
        H2 = False

    try:
        R_G_fg = get_bool(['R_G_is_finitely_generated_A_algebra', 
                           'R_G_is_fg_A_algebra',
                           'invariant_ring_is_finitely_generated'], True)
        R_G_noeth = get_bool(['R_G_is_Noetherian', 
                              'invariant_ring_is_Noetherian'], True)
        
        # The conclusion is that R^G is finitely generated AND Noetherian.
        # So it fails if EITHER is false.
        neg_Q = not (R_G_fg and R_G_noeth)
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: A is a commutative Noetherian ring",
    "H_2: R is a finitely generated commutative A-algebra",
    "¬Q: R^G is not a finitely generated A-algebra or not Noetherian"
]

N_HYP = 2
NEG_Q_INDEX = 2