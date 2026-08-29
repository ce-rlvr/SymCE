import math
from sympy.ntheory import factorint
from sympy import Poly
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: q is an integer >= 2",
    "¬Q: The equivalence (f(x) is a bijection iff gcd(n, q-1) == 1) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Extract n and q from the witness
        if isinstance(witness, dict):
            if 'n' in witness:
                n_val = witness['n']
            elif 'f' in witness:
                n_val = witness['f']
            else:
                return [False, False, False]
            q_val = witness['q']
        elif isinstance(witness, (tuple, list)) and len(witness) >= 2:
            n_val, q_val = witness[-2:]
        else:
            return [False, False, False]
            
        # Parse n (could be an integer or a sympy monomial like x**n)
        try:
            n = int(n_val)
        except Exception:
            p = Poly(n_val)
            if p.is_monomial and p.LC() == 1:
                n = sum(p.monoms()[0])
            else:
                return [False, False, False]
                
        # Parse q
        q = int(q_val)
    except Exception:
        return [False, False, False]
        
    # H_1: n is a positive integer
    try:
        h1 = (n > 0)
    except Exception:
        h1 = False
        
    # H_2: q is an integer >= 2 (so that Z_q is well-defined)
    try:
        h2 = (q >= 2)
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion fails
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            factors = factorint(q)
            if len(factors) == 1:
                # If q is a prime power, F_q is a finite field.
                # The theorem is mathematically true for all finite fields.
                neg_q = False
            else:
                # If q is not a prime power, F_q is undefined but typically interpreted as Z_q.
                # We evaluate the bijection property over Z_q.
                seen = set()
                bijection = True
                for val_x in range(q):
                    val = pow(val_x, n, q)
                    if val in seen:
                        bijection = False
                        break
                    seen.add(val)
                
                gcd_cond = (math.gcd(n, q - 1) == 1)
                
                # The conclusion is an equivalence; it fails if the truth values differ
                neg_q = (bijection != gcd_cond)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]