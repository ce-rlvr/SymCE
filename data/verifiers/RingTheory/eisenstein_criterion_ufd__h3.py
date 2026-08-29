import sympy
from sympy import Poly, factor_list
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain with fraction field K",
    "H_2: f is a polynomial over R of degree n >= 1",
    "H_3: p divides a_i for all 0 <= i < n",
    "H_4: p does not divide a_n",
    "H_5: p^2 does not divide a_0",
    "¬Q: The polynomial f is reducible over the fraction field K"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness) -> list[bool]:
    try:
        p, f = witness
    except Exception:
        return [False] * 6

    # Parse f
    try:
        f_sym = sympy.sympify(f)
        free_symbols = f_sym.free_symbols
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        elif len(free_symbols) > 1:
            if x in free_symbols:
                var = x
            else:
                var = list(free_symbols)[0]
        else:
            var = x
        poly_f = Poly(f_sym, var)
        coeffs = poly_f.all_coeffs()
        n = poly_f.degree()
    except Exception:
        return [False] * 6

    # Parse p
    try:
        p_sym = sympy.sympify(p)
    except Exception:
        return [False] * 6

    # H_1: R is a UFD with fraction field K
    # We verify this by checking if p and all coefficients are integers,
    # which implies they belong to ZZ, a known UFD.
    try:
        h1 = bool(p_sym.is_integer) and all(bool(sympy.sympify(c).is_integer) for c in coeffs)
    except Exception:
        h1 = False

    # H_2: f is a polynomial over R of degree n >= 1
    try:
        h2 = h1 and (n >= 1)
    except Exception:
        h2 = False

    # H_3: p divides a_i for all 0 <= i < n
    try:
        if n >= 1:
            # coeffs are [a_n, a_{n-1}, ..., a_0]
            # a_i for 0 <= i < n are coeffs[1:]
            h3 = all(sympy.sympify(c) % p_sym == 0 for c in coeffs[1:])
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: p does not divide a_n
    try:
        if n >= 0:
            h4 = sympy.sympify(coeffs[0]) % p_sym != 0
        else:
            h4 = False
    except Exception:
        h4 = False

    # H_5: p^2 does not divide a_0
    try:
        if n >= 0:
            h5 = sympy.sympify(coeffs[-1]) % (p_sym**2) != 0
        else:
            h5 = False
    except Exception:
        h5 = False

    # ¬Q: f is reducible over K (which is QQ since R is ZZ)
    try:
        factors = factor_list(poly_f, domain='QQ')
        # Count the total number of non-constant irreducible factors (with multiplicity)
        num_non_constant = sum(exp for poly, exp in factors[1] if poly.degree() >= 1)
        neg_q = num_non_constant >= 2
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]