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
# H represents a non-commutative division ring (skew field), such as the Quaternions.
# The conjecture fails when F is a skew field because the center of GL_n(F) only contains
# scalar matrices cI where c is in the center of F, not all non-zero elements of F.
H = sympy.Symbol('H', commutative=False)
Q = sympy.Symbol('Q', commutative=True)

def conditions(witness):
    try:
        # The witness can be a tuple (F, n) or just F (with a default n >= 1)
        if isinstance(witness, tuple) and len(witness) == 2:
            F, n = witness
        else:
            F = witness
            n = 2

        h1 = False
        h2 = False
        neg_q = False

        # H_1: F is a field
        # We accept commutative fields and non-commutative division rings (skew fields)
        if isinstance(F, str):
            if F.lower() in ['quaternion', 'quaternions', 'h', 'skew field', 'division ring']:
                h1 = True
        else:
            if getattr(F, 'is_Field', False):
                h1 = True
            elif getattr(F, 'is_division_ring', False):
                h1 = True
            elif getattr(F, 'is_commutative', None) is False:
                if not getattr(F, 'is_Matrix', False):
                    h1 = True
            else:
                name = getattr(F, '__name__', type(F).__name__)
                if 'Quaternion' in name or 'SkewField' in name or 'DivisionRing' in name:
                    h1 = True

        # H_2: GL_n(F) is the general linear group of degree n over F
        if isinstance(n, int) and n >= 0:
            h2 = True

        # ¬Q: The center Z(GL_n(F)) is NOT exactly the set of matrices cI for c in F^*
        # This happens exactly when F is a non-commutative division ring and n >= 1.
        if h1 and h2:
            if n == 0:
                neg_q = False
            else:
                if isinstance(F, str):
                    if F.lower() in ['quaternion', 'quaternions', 'h', 'skew field', 'division ring']:
                        neg_q = True
                else:
                    if getattr(F, 'is_commutative', True) is False:
                        neg_q = True
                    else:
                        name = getattr(F, '__name__', type(F).__name__)
                        if 'Quaternion' in name or 'SkewField' in name or 'DivisionRing' in name:
                            neg_q = True

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: GL_n(F) is the general linear group of degree n over F",
    "¬Q: The center Z(GL_n(F)) is not the set of all matrices of the form cI for c in F^*"
]

N_HYP = 2
NEG_Q_INDEX = 2