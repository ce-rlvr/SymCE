import sympy
from sympy import Matrix, eye, zeros, Rational, Integer, Symbol, gcd
from sympy.abc import x, y, z
from sympy.polys.polytools import groebner
import math
import itertools
import functools
import z3

# Top-level setup for named objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # Extract witness: could be a matrix A, or a tuple (A, j)
    if isinstance(witness, tuple):
        if len(witness) == 2:
            A, j = witness
        else:
            A = witness[0]
            j = None
    else:
        A = witness
        j = None

    # Ensure A is a sympy Matrix
    try:
        if not isinstance(A, sympy.MatrixBase):
            A = Matrix(A)
    except Exception:
        pass

    # H_1: R is a commutative ring
    # We assume the domain of the provided matrix is a commutative ring.
    h1 = True

    # H_2: n is an integer strictly greater than 1
    try:
        n = A.shape[0]
        h2 = bool(n > 1)
    except Exception:
        h2 = False

    # H_3: A is an invertible matrix in GL_n(R) with entries a_ij
    try:
        if A.is_square:
            d = A.det()
            if d == 0:
                h3 = False
            else:
                # Check if determinant is a unit in the implied ring
                is_field = any(hasattr(e, 'is_Rational') and e.is_Rational and not e.is_Integer for e in A) or \
                           any(hasattr(e, 'is_Float') and e.is_Float for e in A)
                if is_field:
                    h3 = True
                else:
                    # For Z or Z[x], det must be 1 or -1 to be invertible in GL_n(R)
                    if d == 1 or d == -1:
                        h3 = True
                    else:
                        # If there are symbols, allow any non-zero constant assuming it might be over a field of fractions
                        if any(not (hasattr(e, 'is_Integer') and e.is_Integer) for e in A):
                            h3 = bool(d.is_constant()) if hasattr(d, 'is_constant') else True
                        else:
                            h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The sum of the principal ideals (a_1j) + ... + (a_nj) is NOT equal to R
    try:
        def generates_unit(col):
            # Check if elements generate the unit ideal (i.e., 1 is in the ideal)
            if all(hasattr(e, 'is_Integer') and e.is_Integer for e in col) or all(isinstance(e, int) for e in col):
                g = col[0]
                for e in col[1:]:
                    g = gcd(g, e)
                return abs(g) == 1
            
            if any(hasattr(e, 'is_Rational') and e.is_Rational and not e.is_Integer for e in col):
                return any(e != 0 for e in col)
            
            try:
                gb = groebner(col)
                if len(gb) == 1 and gb[0] == 1:
                    return True
            except Exception:
                pass
            
            try:
                g = col[0]
                for e in col[1:]:
                    g = gcd(g, e)
                if g == 1 or g == -1:
                    return True
            except Exception:
                pass
            
            return False

        if j is not None:
            # Assume j is 1-indexed if it's an integer > 0
            col_idx = j - 1 if isinstance(j, int) and j > 0 else j
            col = list(A[:, col_idx])
            q = generates_unit(col)
        else:
            # If j is not specified, check if ALL columns generate the unit ideal
            q = all(generates_unit(list(A[:, c])) for c in range(n))
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is an integer strictly greater than 1",
    "H_3: A is an invertible matrix in GL_n(R) with entries a_ij",
    "¬Q: The sum of the principal ideals (a_1j) + ... + (a_nj) is not equal to R"
]

N_HYP = 3
NEG_Q_INDEX = 3