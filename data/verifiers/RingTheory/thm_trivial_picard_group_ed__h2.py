import sympy
from sympy import Poly
from sympy.abc import x
import math

# Top-level setup
Z = sympy.ZZ
Q = sympy.QQ

def conditions(witness):
    """
    Checks if the witness is an integral domain with a non-trivial Picard group.
    The witness is expected to be an integer d (representing Z[sqrt(d)]) 
    or a SymPy polynomial P(x) (representing Z[x]/(P(x))).
    """
    try:
        if isinstance(witness, (int, sympy.Integer)):
            P = Poly(x**2 - witness, x, domain='ZZ')
        elif hasattr(witness, 'base_ideal'):
            gens = witness.base_ideal.gens
            syms = list(gens[0].free_symbols)
            var = syms[0] if syms else x
            P = Poly(gens[0], var, domain='ZZ')
        elif hasattr(witness, 'free_symbols'):
            syms = list(witness.free_symbols)
            var = syms[0] if syms else x
            P = Poly(witness, var, domain='ZZ')
        else:
            P = Poly(witness, x, domain='ZZ')
    except Exception:
        return [False, False]

    # H_1: R is an integral domain
    # Z[x]/(P) is an integral domain iff P is irreducible over Z.
    try:
        h1 = bool(P.is_irreducible)
    except Exception:
        h1 = False

    # ¬Q: The Picard group Pic(R) is NOT trivial
    # For a quadratic order Z[x]/(ax^2+bx+c), the Picard group is isomorphic 
    # to the form class group of discriminant D = b^2 - 4ac.
    try:
        if P.degree() != 2:
            neg_q = False
        else:
            coeffs = P.all_coeffs()
            a, b, c = int(coeffs[0]), int(coeffs[1]), int(coeffs[2])
            D = b**2 - 4*a*c
            
            if D >= 0:
                # We only support imaginary quadratic orders for this check
                neg_q = False
            else:
                # Compute the class number h(D) by counting primitive reduced positive-definite forms
                h = 0
                max_a = int((-D / 3.0) ** 0.5)
                for a_form in range(1, max_a + 1):
                    for b_form in range(-a_form, a_form + 1):
                        rem = b_form**2 - D
                        if rem % (4 * a_form) == 0:
                            c_form = rem // (4 * a_form)
                            if c_form >= a_form:
                                if c_form == a_form and b_form < 0:
                                    continue
                                if a_form == abs(b_form) and b_form < 0:
                                    continue
                                # Check primitivity: gcd(a, b, c) == 1
                                if math.gcd(math.gcd(a_form, b_form), c_form) == 1:
                                    h += 1
                neg_q = (h > 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The Picard group Pic(R) is not trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1