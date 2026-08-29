import sympy
from sympy.polys.domains import ZZ, QQ
from sympy import isprime, factor_list
from sympy.abc import x, y, z

def conditions(witness):
    try:
        # The witness can be a tuple (R, p) or just an element p (defaulting to R = ZZ)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, p = witness
            if R == sympy.S.Integers:
                R = ZZ
            elif R == sympy.S.Rationals:
                R = QQ
        else:
            R = ZZ
            p = witness
    except Exception:
        return [False, False]

    # H_1: R is a unique factorization domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # ¬Q: p is not a prime element in R
    try:
        is_prime = False
        if p == 0 or p == getattr(R, 'zero', None):
            is_prime = False
        elif R == ZZ:
            try:
                if p not in ZZ:
                    return [h1, False]
                val = abs(int(p))
                if val == 1:
                    is_prime = False
                else:
                    is_prime = isprime(val)
            except Exception:
                return [h1, False]
        else:
            try:
                if hasattr(R, 'to_sympy'):
                    expr = R.to_sympy(p)
                else:
                    expr = p
                
                f_list = factor_list(expr, domain=R)
                content = f_list[0]
                factors = f_list[1]
                
                content_is_unit = False
                try:
                    if hasattr(R, 'is_unit'):
                        content_is_unit = R.is_unit(R(content))
                    elif R == ZZ:
                        content_is_unit = (abs(content) == 1)
                    else:
                        if hasattr(R, 'is_Field') and R.is_Field:
                            content_is_unit = (content != 0)
                        else:
                            content_is_unit = (content == 1 or content == -1)
                except Exception:
                    content_is_unit = (content == 1 or content == -1)
                    
                if len(factors) == 0:
                    # Only content, no variables -> it's a unit or zero
                    is_prime = False
                elif len(factors) == 1 and factors[0][1] == 1:
                    # One irreducible factor of multiplicity 1. 
                    # It is prime iff the content is a unit.
                    is_prime = content_is_unit
                else:
                    is_prime = False
            except Exception:
                # If factor_list fails, p is likely not a valid element of R
                return [h1, False]
                
        neg_q = not is_prime
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: p is not a prime element in R"
]

N_HYP = 1
NEG_Q_INDEX = 1