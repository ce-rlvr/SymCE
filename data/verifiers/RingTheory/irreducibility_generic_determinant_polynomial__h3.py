import sympy
from sympy import Matrix, Symbol
from sympy.polys.polytools import factor_list

# Top-level setup
# The witness is expected to be a sympy Matrix M, or a tuple containing M.
# The entries of M are elements of a UFD (e.g., polynomials over ZZ or QQ).

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            M = witness[-1]
        else:
            M = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a unique factorization domain
    # We assume the witness is constructed over a UFD (like ZZ or QQ).
    try:
        h1_ok = isinstance(M, Matrix)
    except Exception:
        h1_ok = False

    # H2: n is an integer such that n >= 2
    try:
        n = M.rows
        h2_ok = (n >= 2) and (M.cols == n)
    except Exception:
        h2_ok = False

    # H3: M is the n x n matrix with entries X_ij
    try:
        h3_ok = isinstance(M, Matrix) and M.is_square
    except Exception:
        h3_ok = False

    # neg_Q: The determinant polynomial det(M) is NOT irreducible in R[{X_ij}]
    try:
        det_M = M.det()
        if det_M == 0:
            neg_q = True
        else:
            # Factor the determinant
            coeff, factors = factor_list(det_M)
            
            # Count the total number of non-constant irreducible factors (with multiplicity)
            num_poly_factors = sum(exp for poly, exp in factors if not poly.is_constant())
            
            # A polynomial is reducible if it has more than one non-constant factor,
            # or if it is a constant (0 non-constant factors).
            # If the base ring is ZZ, a non-unit constant content also makes it reducible,
            # but checking polynomial factors is usually sufficient for these counterexamples.
            if num_poly_factors > 1 or num_poly_factors == 0:
                neg_q = True
            else:
                # Check if the content is a non-unit (e.g., in ZZ, content != 1 and != -1)
                # If coeff is not 1 or -1, and we are over ZZ, it's reducible.
                # We'll assume it's reducible if coeff is not 1 or -1.
                if coeff != 1 and coeff != -1:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: n is an integer such that n >= 2",
    "H_3: M is the n x n matrix with entries X_ij",
    "¬Q: The determinant polynomial det(M) is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3