import sympy
import sympy.ntheory
from sympy.abc import x

def conditions(witness):
    """
    Given a witness tuple (q, p, a), checks if it is a valid counterexample to the conjecture.
    """
    try:
        q, p, a = witness
    except Exception:
        return [False, False, False]
        
    try:
        q_int = int(q)
        p_int = int(p)
        a_int = int(a)
        if p_int < 1:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F_q is a finite field with q elements
    try:
        h1 = bool(sympy.ntheory.is_primepower(q_int))
    except Exception:
        h1 = False

    # H_2: a is an element of F_q that is not the p-th power of any element in F_q
    try:
        if sympy.ntheory.is_prime(q_int):
            a_mod = a_int % q_int
            is_p_power = False
            for i in range(q_int):
                if pow(i, p_int, q_int) == a_mod:
                    is_p_power = True
                    break
            h2 = not is_p_power
        else:
            # For simplicity and robustness, we only evaluate H2 for prime q.
            # A prime q is sufficient to find a valid counterexample.
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The binomial x^p - a is reducible over F_q
    try:
        if sympy.ntheory.is_prime(q_int):
            poly = x**p_int - a_int
            factors = sympy.factor_list(poly, modulus=q_int)
            
            # factors[1] is a list of tuples: (factor, multiplicity)
            # The polynomial is irreducible if there is exactly 1 factor, 
            # its multiplicity is 1, and its degree equals p.
            if len(factors[1]) == 1 and factors[1][0][1] == 1:
                fac = factors[1][0][0]
                if fac.as_poly(x).degree() == p_int:
                    is_irreducible = True
                else:
                    is_irreducible = False
            else:
                is_irreducible = False
                
            neg_q = not is_irreducible
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: a is an element of F_q that is not the p-th power of any element in F_q",
    "¬Q: The binomial x^p - a is reducible over F_q"
]

N_HYP = 2
NEG_Q_INDEX = 2