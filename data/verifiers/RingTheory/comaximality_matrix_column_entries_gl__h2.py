import sympy
from sympy import Matrix, gcd
from sympy.polys.polytools import groebner

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    """
    h1 = h2 = h3 = neg_q = False

    # 1. Try duck typing for a fully custom witness object
    try:
        if hasattr(witness, 'h1'):
            h1 = witness.h1() if callable(witness.h1) else witness.h1
            h2 = witness.h2() if callable(witness.h2) else witness.h2
            h3 = witness.h3() if callable(witness.h3) else witness.h3
            neg_q = witness.neg_q() if callable(witness.neg_q) else witness.neg_q
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass

    # 2. Try unpacking the witness
    A = None
    j = 1
    R_units = None
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                A, j = witness
            elif len(witness) >= 3:
                A, j, R_units = witness[0], witness[1], witness[2]
        else:
            A = witness
    except Exception:
        pass

    # H1: R is a commutative ring
    try:
        if hasattr(A, 'is_commutative_ring'):
            h1 = A.is_commutative_ring()
        else:
            # Standard sympy expressions commute
            h1 = True
    except Exception:
        h1 = False

    # H2: A is an invertible matrix in GL_n(R)
    try:
        if hasattr(A, 'is_invertible_in_GLn'):
            h2 = A.is_invertible_in_GLn()
        elif isinstance(A, Matrix):
            d = A.det()
            if R_units is not None and d in R_units:
                h2 = True
            elif d == 1 or d == -1:
                h2 = True
            elif hasattr(d, 'is_constant') and d.is_constant() and d != 0:
                h2 = True
            else:
                try:
                    A_inv = A.inv()
                    h2 = True
                except Exception:
                    h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: j is a fixed column index such that 1 <= j <= n
    try:
        if hasattr(A, 'is_valid_column_index'):
            h3 = A.is_valid_column_index(j)
        elif isinstance(A, Matrix):
            n = A.shape[1]
            h3 = (1 <= j <= n)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The sum of the principal ideals is NOT equal to R
    try:
        if hasattr(A, 'sum_of_ideals_is_R'):
            neg_q = not A.sum_of_ideals_is_R(j)
        elif isinstance(A, Matrix):
            col = list(A[:, j-1])
            g = col[0]
            for i in range(1, len(col)):
                g = gcd(g, col[i])
            
            if R_units is not None and g in R_units:
                neg_q = False
            elif g == 1 or g == -1:
                neg_q = False
            else:
                try:
                    gb = groebner(col)
                    if len(gb) == 1 and (gb[0] == 1 or gb[0] == -1 or (R_units is not None and gb[0] in R_units)):
                        neg_q = False
                    else:
                        neg_q = True
                except Exception:
                    neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: A is an invertible matrix in GL_n(R)",
    "H_3: j is a fixed column index such that 1 <= j <= n",
    "¬Q: The sum of the principal ideals is not equal to R"
]

N_HYP = 3
NEG_Q_INDEX = 3