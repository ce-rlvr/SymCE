import math
from sympy import cyclotomic_poly, factor_list, isprime, degree
from sympy.abc import x
from sympy.ntheory import totient, n_order, factorint

def conditions(witness):
    """
    Given a witness (n, p, d) or (n, p), checks if it is a valid counterexample to the conjecture.
    """
    n = p = d = None
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                n, p, d = witness
            elif len(witness) == 2:
                n, p = witness
                if isinstance(n, int) and isinstance(p, int) and n > 0 and math.gcd(p, n) == 1:
                    d = n_order(p, n)
                else:
                    d = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n > 0
    except Exception:
        h1 = False

    # H_2: d is the multiplicative order of p modulo n
    try:
        if d is not None and isinstance(p, int) and isinstance(n, int) and n > 0 and math.gcd(p, n) == 1:
            h2 = (d == n_order(p, n))
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails at the witness
    # Conclusion: Phi_n(x) factors over F_p into exactly phi(n)/d distinct irreducible polynomials of degree d.
    try:
        if not isinstance(p, int) or isinstance(p, bool) or p < 2:
            q_ok = False
        else:
            factors_p = factorint(p)
            if len(factors_p) != 1:
                # p is not a prime power, so F_p is not a finite field.
                # The premise of the conclusion fails, making the statement false.
                q_ok = False
            else:
                if isprime(p):
                    # p is prime, we can verify the factorization over F_p
                    poly = cyclotomic_poly(n, x)
                    fact = factor_list(poly, modulus=p)
                    expected_count = totient(n) // d
                    
                    if len(fact[1]) != expected_count:
                        q_ok = False
                    else:
                        q_ok = True
                        for f, mult in fact[1]:
                            if mult != 1:
                                q_ok = False
                                break
                            if degree(f) != d:
                                q_ok = False
                                break
                else:
                    # p is a prime power but not prime.
                    # The theorem mathematically holds for all prime powers q coprime to n.
                    if math.gcd(p, n) == 1:
                        q_ok = True
                    else:
                        q_ok = False
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: d is the multiplicative order of p modulo n",
    "¬Q: Phi_n(x) does not factor into exactly phi(n)/d distinct irreducible polynomials of degree d over F_p"
]

N_HYP = 2
NEG_Q_INDEX = 2