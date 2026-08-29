import sympy
from sympy.abc import x, y, z
import math
from functools import reduce

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, P = witness
            else:
                return [False, False]
        else:
            R = ZZ
            P = witness

        # H1: R is an integral domain
        h1 = False
        if R == ZZ or R == QQ:
            h1 = True
        elif hasattr(R, 'is_domain'):
            h1 = bool(R.is_domain)
        else:
            h1 = True # Assume it's a domain if passed as R

        # Handle P being a list/tuple/set of generators
        if isinstance(P, (list, tuple, set)):
            if len(P) == 1:
                P = list(P)[0]
            elif R == ZZ:
                P = reduce(sympy.gcd, P)
            else:
                pass

        # neg_Q: The polynomial ideal over P is NOT a prime ideal
        # The ideal of polynomials with coefficients in P is prime iff P is a prime ideal in R.
        is_prime_ideal = False
        if R == ZZ:
            try:
                val = abs(int(P))
                is_prime_ideal = sympy.isprime(val) or val == 0
            except Exception:
                pass
        elif getattr(R, 'is_Field', False) or R == QQ:
            try:
                is_prime_ideal = (P == 0 or P == getattr(R, 'zero', 0))
            except Exception:
                pass
        else:
            if P == 0 or P == getattr(R, 'zero', 0):
                is_prime_ideal = True
            else:
                try:
                    if hasattr(R, 'is_irreducible'):
                        is_prime_ideal = R.is_irreducible(P)
                except Exception:
                    pass
                
                if not is_prime_ideal and isinstance(P, sympy.Expr):
                    try:
                        factors = sympy.factor_list(P)
                        if len(factors[1]) == 1 and factors[1][0][1] == 1 and abs(factors[0]) == 1:
                            is_prime_ideal = True
                    except Exception:
                        pass

        neg_q = not is_prime_ideal

        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The polynomial ideal over P is not prime"
]

N_HYP = 1
NEG_Q_INDEX = 1