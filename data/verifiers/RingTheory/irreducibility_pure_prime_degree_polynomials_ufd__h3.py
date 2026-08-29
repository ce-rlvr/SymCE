import sympy
from sympy.abc import x

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: p is a prime element in R",
    "¬Q: The polynomial x^n - p is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    R, p, n = None, None, None
    
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            n = witness.get('n')
            R = witness.get('R', ZZ)
        elif hasattr(witness, 'p') and hasattr(witness, 'n'):
            p = witness.p
            n = witness.n
            R = getattr(witness, 'R', ZZ)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                p, n = witness[0], witness[1]
                R = ZZ
            elif len(witness) == 3:
                R, p, n = witness[0], witness[1], witness[2]
    except Exception:
        pass

    # H_1: R is a unique factorization domain
    try:
        if R is None:
            h1 = False
        elif R == ZZ or R == 'ZZ':
            h1 = True
        elif R == QQ or R == 'QQ':
            h1 = True
        elif hasattr(R, 'is_UFD'):
            h1 = bool(R.is_UFD)
        else:
            h1 = True  # Fallback assumption if we cannot strictly verify the domain type
    except Exception:
        h1 = False

    # H_2: p is a prime element in R
    try:
        if p is None:
            h2 = False
        elif R == QQ or R == 'QQ':
            h2 = False  # Fields have no prime elements
        else:
            p_val = int(p)
            h2 = sympy.isprime(abs(p_val))
    except Exception:
        h2 = False

    # ¬Q: The polynomial x^n - p is reducible
    try:
        if p is None or n is None:
            neg_q = False
        else:
            n_val = int(n)
            p_val = int(p)
            
            if n_val < 0:
                neg_q = True  # Not a polynomial, so it cannot be an irreducible polynomial
            elif n_val == 0:
                # For n = 0, the polynomial is the constant 1 - p.
                # A constant polynomial is reducible if it is reducible in R.
                val = 1 - p_val
                abs_val = abs(val)
                if abs_val <= 1:
                    neg_q = True  # Units and 0 are not irreducible
                else:
                    neg_q = not sympy.isprime(abs_val)
            else:
                # For n >= 1, Eisenstein's criterion guarantees x^n - p is irreducible over any UFD.
                poly = x**n_val - p_val
                neg_q = not sympy.polys.polytools.is_irreducible(poly, domain='ZZ')
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]