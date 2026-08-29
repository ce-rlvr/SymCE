import sympy
from sympy import Symbol, cyclotomic_poly, totient, factor_list, degree

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    The witness is expected to be an integer n.
    """
    # H_1: n is a positive integer
    try:
        n = witness
        h1 = type(n) is int and n > 0
    except Exception:
        h1 = False

    # ¬Q: The extension Q(zeta_n)/Q is NOT a Galois extension of degree phi(n),
    # or its Galois group is NOT isomorphic to (Z/nZ)^times.
    # Since Q(zeta_n) is the splitting field of x^n - 1, it is always Galois.
    # The degree is phi(n) and the Galois group is (Z/nZ)^times if and only if
    # the n-th cyclotomic polynomial is irreducible over Q and has degree phi(n).
    try:
        if not h1:
            neg_q = False
        else:
            poly = cyclotomic_poly(n, x)
            deg = degree(poly)
            expected_deg = totient(n)
            
            deg_correct = (deg == expected_deg)
            
            # factor_list over Q (default for integer coefficients)
            factors = factor_list(poly)
            is_irreducible = (len(factors[1]) == 1 and factors[1][0][1] == 1)
            
            q = deg_correct and is_irreducible
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: Q(zeta_n)/Q is not a Galois extension of degree phi(n) or its Galois group is not isomorphic to (Z/nZ)^times"
]

N_HYP = 1
NEG_Q_INDEX = 1