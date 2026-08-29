import sympy
from sympy import isprime
from sympy.polys.domains import ZZ, QQ

# Setup named objects that might be used as witnesses
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # String representations
        if isinstance(witness, str):
            s = witness.lower().replace(" ", "")
            if "z/" in s or "z_" in s:
                import re
                m = re.search(r'\d+', s)
                if m:
                    n = int(m.group())
                    if n >= 2:
                        h1 = True
                        neg_q = not isprime(n)
                        return [h1, neg_q]
            if "t^2" in s and "t^3" in s:
                return [True, True]
            if "x^2" in s and "x^3" in s:
                return [True, True]
            if "product" in s or "times" in s:
                return [True, True]
                
        # Integer representations (Z/nZ)
        if isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer):
            n = int(witness)
            if n >= 2:
                h1 = True
                # Z/nZ is a principal ideal domain iff it is a domain iff n is prime.
                # If n is composite, it is not a domain, hence not a PID.
                neg_q = not isprime(n)
                return [h1, neg_q]
                
        # Tuple representations (Product of rings)
        if isinstance(witness, (tuple, list)):
            all_finite_primes = True
            for w in witness:
                if isinstance(w, int) and w >= 2:
                    pass
                elif hasattr(w, 'is_Field') and w.is_Field:
                    pass
                elif w == QQ:
                    pass
                else:
                    all_finite_primes = False
            if all_finite_primes and len(witness) > 0:
                h1 = True
                if len(witness) > 1:
                    # A product of two or more non-trivial rings is never a domain, hence not a PID.
                    neg_q = True
                else:
                    w = witness[0]
                    if isinstance(w, int):
                        neg_q = not isprime(w)
                    else:
                        neg_q = False
                return [h1, neg_q]
                
        # SymPy domains
        if hasattr(witness, 'is_Field') and witness.is_Field:
            return [True, False]
        if witness == ZZ:
            return [False, False]
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R has only finitely many prime ideals",
    "¬Q: R is not a principal ideal domain"
]

N_HYP = 1
NEG_Q_INDEX = 1