import sympy
from sympy import ZZ, QQ

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to:
    "Let M be a flat module over R. Then M is a torsion-free module."
    
    When the hypothesis that R is a domain is dropped, a standard counterexample 
    is R = Z/nZ for a composite integer n, and M = R. 
    M is free (hence flat) over R, but has torsion elements because R has zero divisors.
    """
    h1 = False
    neg_q = False
    
    try:
        # If witness is a sympy domain (like ZZ, QQ)
        if hasattr(witness, 'is_domain'):
            h1 = True
            neg_q = not bool(witness.is_domain)
            return [h1, neg_q]
    except Exception:
        pass

    try:
        # If witness is an integer n, it represents R = M = Z/nZ
        if isinstance(witness, (tuple, list)):
            n = int(witness[0])
        else:
            n = int(witness)
            
        if n == 0:
            # R = Z, which is a domain
            h1 = True
            neg_q = False
            return [h1, neg_q]
        elif n > 1:
            # R = Z/nZ is a flat module over itself.
            h1 = True
            # M is torsion-free iff R is a domain, which means n is prime.
            # Thus, M is NOT torsion-free iff n is composite.
            neg_q = not sympy.isprime(n)
            return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: M is a flat module over R",
    "¬Q: M is not a torsion-free module"
]

N_HYP = 1
NEG_Q_INDEX = 1