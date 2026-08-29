import sympy
from sympy import cyclotomic_poly, factor_list, degree
from sympy.ntheory import totient, isprime
from sympy.abc import x

# No specific named objects needed for this field theory conjecture.
# Witnesses are expected to be tuples of the form (n, p, d) or dictionaries.

def conditions(witness):
    """
    Given a witness (n, p, d), check the remaining hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
            d = witness.get('d')
        else:
            n, p, d = witness
    except Exception:
        return [False, False, False]

    # H_1: n is a positive integer
    try:
        h1_ok = (int(n) == n) and (n > 0)
    except Exception:
        h1_ok = False

    # H_2: p is a prime number that does not divide n
    try:
        h2_ok = isprime(p) and (n % p != 0)
    except Exception:
        h2_ok = False

    # neg_Q: The cyclotomic polynomial Phi_n(x) does NOT factor over F_p into 
    # exactly phi(n)/d distinct irreducible polynomials, each of degree d.
    try:
        if int(d) != d or d <= 0:
            neg_q_ok = True
        else:
            d = int(d)
            phi_n = totient(n)
            
            if phi_n % d != 0:
                neg_q_ok = True
            else:
                expected_count = phi_n // d
                poly = cyclotomic_poly(n, x)
                factors = factor_list(poly, modulus=p)
                
                is_Q_true = True
                # Check if the number of irreducible factors matches expected_count
                if len(factors[1]) != expected_count:
                    is_Q_true = False
                else:
                    for f, mult in factors[1]:
                        # Check if factors are distinct (multiplicity 1)
                        if mult != 1:
                            is_Q_true = False
                            break
                        # Check if each factor has degree exactly d
                        if degree(f, x) != d:
                            is_Q_true = False
                            break
                            
                neg_q_ok = not is_Q_true
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: p is a prime number that does not divide n",
    "¬Q: Phi_n(x) does not factor over F_p into exactly phi(n)/d distinct irreducible polynomials of degree d"
]

N_HYP = 2
NEG_Q_INDEX = 2