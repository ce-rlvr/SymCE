import sympy
from sympy import isprime, bernoulli, minpoly, Dummy, exp, I, pi, im, simplify, N

# Top-level setup
# No special named objects needed for this specific number theory / field theory conjecture,
# but we import standard SymPy tools.

def conditions(witness):
    """
    Checks whether the given witness is a counterexample to the false conjecture.
    The witness should be a tuple (p, u), where p is a prime and u is a unit.
    """
    try:
        p, u = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a regular prime number
    try:
        if not isprime(p):
            h1_ok = False
        else:
            h1_ok = True
            if p > 2:
                for k in range(2, p - 1, 2):
                    num, den = bernoulli(k).as_numer_denom()
                    if num % p == 0:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # H_2: u is a unit in the ring of integers of the cyclotomic field Q(zeta_p)
    try:
        x = Dummy('x')
        poly = minpoly(u, x)
        coeffs = poly.all_coeffs()
        # A unit in the ring of integers must be an algebraic integer (monic minpoly with integer coeffs)
        # and its norm (constant term) must be +/- 1.
        if all(c.is_integer for c in coeffs) and abs(coeffs[-1]) == 1:
            h2_ok = True
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # neg_Q: The unit u CANNOT be written in the form u = zeta_p^k * r, 
    # where k is an integer and r is a real unit in Q(zeta_p).
    # If it CAN be written in this form, then for some k, u * zeta_p^(-k) is real.
    try:
        zeta = exp(2 * I * pi / p)
        neg_q_ok = True
        for k in range(p):
            r = u * zeta**(-k)
            im_r = im(r)
            
            # Check if imaginary part is exactly zero
            if im_r.is_zero:
                neg_q_ok = False
                break
            
            # Check with simplification
            im_r_simp = simplify(im_r)
            if im_r_simp.is_zero:
                neg_q_ok = False
                break
            
            # Check numerically as a fallback
            val = complex(N(im_r, 100))
            if abs(val) < 1e-80:
                neg_q_ok = False
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a regular prime number",
    "H_2: u is a unit in the ring of integers of the cyclotomic field Q(zeta_p)",
    "¬Q: u cannot be written in the form u = zeta_p^k * r where r is a real unit"
]

N_HYP = 2
NEG_Q_INDEX = 2