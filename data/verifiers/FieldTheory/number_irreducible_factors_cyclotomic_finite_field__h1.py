import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
x = sympy.abc.x

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple/list (n, p, d) or a dict with these keys.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
            d = witness.get('d')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            n, p, d = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number that does not divide n
    try:
        n_int = int(n)
        p_int = int(p)
        h1 = sympy.isprime(p_int) and (n_int % p_int != 0)
    except Exception:
        h1 = False
        
    # H_2: d is the multiplicative order of p modulo n
    try:
        n_int = int(n)
        p_int = int(p)
        d_int = int(d)
        if n_int == 0:
            h2 = False
        else:
            abs_n = abs(n_int)
            if abs_n == 1:
                actual_d = 1
            else:
                if math.gcd(p_int, abs_n) != 1:
                    actual_d = None
                else:
                    actual_d = sympy.ntheory.n_order(p_int, abs_n)
            h2 = (d_int == actual_d)
    except Exception:
        h2 = False
        
    # ¬Q: The cyclotomic polynomial Phi_n(x) does NOT factor over F_p into exactly 
    #     phi(n)/d distinct irreducible polynomials of degree d.
    try:
        n_int = int(n)
        p_int = int(p)
        d_int = int(d)
        
        phi_n = sympy.totient(n_int)
        if phi_n % d_int != 0:
            neg_q = True
        else:
            expected_count = phi_n // d_int
            poly = sympy.cyclotomic_poly(n_int, x)
            coeff, factors = sympy.factor_list(poly, modulus=p_int)
            
            if len(factors) != expected_count:
                neg_q = True
            else:
                all_match = True
                for f, mult in factors:
                    if mult != 1:
                        all_match = False
                        break
                    if f.as_poly(x).degree() != d_int:
                        all_match = False
                        break
                neg_q = not all_match
    except Exception:
        # If cyclotomic_poly is undefined (e.g., for n <= 0), the conclusion fails.
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number that does not divide n",
    "H_2: d is the multiplicative order of p modulo n",
    "¬Q: The cyclotomic polynomial Phi_n(x) does not factor over F_p into exactly phi(n)/d distinct irreducible polynomials of degree d"
]

N_HYP = 2
NEG_Q_INDEX = 2