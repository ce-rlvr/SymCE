import sympy
from sympy import I, pi, exp, Rational
from sympy.abc import x, y, z

def is_zero(expr):
    """
    Safely checks if a sympy expression or complex number is zero.
    """
    try:
        if expr == 0:
            return True
        simp = sympy.simplify(expr)
        if simp == 0:
            return True
        # Fallback to numerical evaluation for complex expressions
        num = complex(simp.evalf())
        if abs(num) < 1e-12:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple: (p, n, zeta_n, sigma_p)
    where sigma_p can be a callable, a dictionary, or the evaluated image sigma_p(zeta_n).
    """
    try:
        p, n, zeta_n, sigma_p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number that does not divide n
    # Note: In the context of this counterexample, p may be a negative prime.
    try:
        p_val = int(p)
        n_val = int(n)
        if p_val != p or n_val != n:
            h1 = False
        else:
            h1 = sympy.isprime(abs(p_val)) and (n_val % p_val != 0)
    except Exception:
        h1 = False

    # H_2: zeta_n is a primitive n-th root of unity in C
    try:
        n_val = int(n)
        if n_val != n:
            h2 = False
        else:
            n_abs = abs(n_val)
            if n_abs == 0:
                h2 = False
            else:
                # Check if zeta_n^n == 1
                if not is_zero(zeta_n**n_abs - 1):
                    h2 = False
                else:
                    h2 = True
                    # Check that zeta_n^d != 1 for all proper divisors d
                    factors = sympy.factorint(n_abs)
                    for q in factors:
                        d = n_abs // q
                        if is_zero(zeta_n**d - 1):
                            h2 = False
                            break
    except Exception:
        h2 = False

    def get_val(sigma, z_val):
        if callable(sigma):
            return sigma(z_val)
        elif isinstance(sigma, dict):
            return sigma[z_val]
        else:
            return sigma

    # H_3: sigma_p is the Frobenius automorphism at p in Gal(Q(zeta_n)/Q)
    # The Frobenius automorphism at p maps zeta_n to zeta_n^{|p|}
    try:
        val = get_val(sigma_p, zeta_n)
        expected_H3 = zeta_n**abs(int(p))
        h3 = is_zero(val - expected_H3)
    except Exception:
        h3 = False

    # neg_Q: The conclusion sigma_p(zeta_n) = zeta_n^p FAILS
    try:
        val = get_val(sigma_p, zeta_n)
        expected_Q = zeta_n**int(p)
        neg_q = not is_zero(val - expected_Q)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number that does not divide n",
    "H_2: zeta_n is a primitive n-th root of unity in C",
    "H_3: sigma_p is the Frobenius automorphism at p in Gal(Q(zeta_n)/Q)",
    "¬Q: sigma_p(zeta_n) != zeta_n^p"
]

N_HYP = 3
NEG_Q_INDEX = 3