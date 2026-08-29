import sympy
from sympy import abc

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "Every element in a Euclidean domain is a prime element."
    
    The witness can be an element p (e.g., an integer or a polynomial),
    or a tuple (R, p). We infer the Euclidean domain from p.
    """
    # Extract p if witness is a tuple
    if isinstance(witness, tuple) and len(witness) == 2:
        _, p = witness
    else:
        p = witness

    # H_1: R is a Euclidean domain
    # We interpret integers as elements of ZZ, and univariate polynomials as elements of QQ[x].
    # Both ZZ and QQ[x] are Euclidean domains.
    try:
        if isinstance(p, (int, sympy.Integer, sympy.Rational)):
            h1 = True
        elif hasattr(p, 'is_polynomial') and p.is_polynomial():
            # Univariate polynomials over a field (like QQ) form a Euclidean domain.
            # Multivariate polynomials do not.
            if len(p.free_symbols) <= 1:
                h1 = True
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: p is not a prime element in R
    try:
        if isinstance(p, (int, sympy.Integer)):
            val = abs(int(p))
            is_prime = sympy.isprime(val)
        elif isinstance(p, sympy.Rational):
            # In a field like QQ, non-zero elements are units, hence not prime.
            is_prime = False
        elif hasattr(p, 'is_polynomial') and p.is_polynomial():
            if len(p.free_symbols) == 1:
                # Check primality (irreducibility) in QQ[x]
                poly = sympy.Poly(p, domain='QQ')
                if poly.is_zero:
                    is_prime = False
                elif poly.degree() <= 0:
                    is_prime = False
                else:
                    factors = sympy.factor_list(poly)
                    # It is prime if there is exactly one irreducible factor with multiplicity 1
                    if len(factors[1]) == 1 and factors[1][0][1] == 1:
                        is_prime = True
                    else:
                        is_prime = False
            else:
                is_prime = False
        else:
            is_prime = False
            
        neg_q = not is_prime
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: p is not a prime element in R"
]

N_HYP = 1
NEG_Q_INDEX = 1