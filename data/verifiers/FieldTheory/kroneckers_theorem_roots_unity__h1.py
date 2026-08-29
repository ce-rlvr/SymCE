import sympy
from sympy import minpoly, Poly, I, Abs
from sympy.abc import x
from sympy.polys import cyclotomic_poly
from sympy.ntheory import totient
from sympy.combinatorics.named_groups import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: Every Galois conjugate of alpha has an absolute value exactly equal to 1 in the complex plane",
    "¬Q: alpha is not a root of unity"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # H1: Every Galois conjugate of alpha has an absolute value exactly equal to 1
    h1_ok = False
    try:
        p = minpoly(witness, x)
        p_poly = Poly(p, x)
        rts = p_poly.nroots(n=60)
        if rts:
            h1_ok = True
            for r in rts:
                if abs(abs(r) - 1) > 1e-40:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # neg_Q: alpha is NOT a root of unity
    neg_q_ok = False
    try:
        p = minpoly(witness, x)
        p_poly = Poly(p, x)
        
        is_root_of_unity = False
        
        # A root of unity must be an algebraic integer, so its minimal monic polynomial
        # over the rationals must have integer coefficients.
        is_alg_int = True
        for c in p_poly.all_coeffs():
            if not c.is_Integer:
                is_alg_int = False
                break
                
        if is_alg_int:
            d = p_poly.degree()
            # If it is a root of unity, its minimal polynomial must be a cyclotomic polynomial.
            # The degree of the n-th cyclotomic polynomial is totient(n).
            # We check all candidate n where totient(n) == d.
            for n in range(1, 3 * d**2 + 5):
                if totient(n) == d:
                    if p == cyclotomic_poly(n, x):
                        is_root_of_unity = True
                        break
        
        neg_q_ok = not is_root_of_unity
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]