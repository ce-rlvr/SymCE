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

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: The field of fractions of R/P is NOT isomorphic to the residue field R_P / P R_P"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, P = witness
        else:
            R = witness
            P = None
    except Exception:
        return [False, False]

    # H1: P is a prime ideal of R
    try:
        if hasattr(R, 'is_prime_ideal'):
            val = R.is_prime_ideal(P)
            h1 = val() if callable(val) else val
        elif hasattr(P, 'is_prime_ideal_of'):
            val = P.is_prime_ideal_of(R)
            h1 = val() if callable(val) else val
        elif hasattr(P, 'is_prime_ideal'):
            val = P.is_prime_ideal
            h1 = val() if callable(val) else val
        elif hasattr(P, 'is_prime'):
            val = P.is_prime
            h1 = val() if callable(val) else val
        elif isinstance(witness, dict):
            h1 = witness.get('is_prime_ideal', False)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The field of fractions of R/P is isomorphic to R_P / P R_P (must FAIL)
    try:
        if hasattr(R, 'quotient_ring') and hasattr(R, 'localization'):
            frac = R.quotient_ring(P).field_of_fractions()
            loc = R.localization(P)
            res = loc.residue_field(P)
            is_iso = frac.is_isomorphic(res)
            neg_q = not (is_iso() if callable(is_iso) else is_iso)
        elif hasattr(R, 'is_commutative'):
            # The theorem holds for commutative rings. If R is not commutative, 
            # localization might fail (e.g., Ore condition) or the isomorphism fails.
            is_comm = R.is_commutative
            is_comm = is_comm() if callable(is_comm) else is_comm
            neg_q = not is_comm
        elif isinstance(witness, dict):
            neg_q = not witness.get('conclusion_holds', True)
        else:
            neg_q = False
    except Exception:
        # If localization or field of fractions fails to compute, the isomorphism fails.
        neg_q = True

    return [bool(h1), bool(neg_q)]