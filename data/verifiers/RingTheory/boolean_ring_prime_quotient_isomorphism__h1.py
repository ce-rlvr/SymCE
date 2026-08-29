import sympy
from sympy import isprime, gcd
from sympy.abc import x, y, z

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ
Z = 0
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z10 = 10
Z12 = 12

def extract_number(s):
    num_str = ""
    for char in s:
        if char.isdigit():
            num_str += char
        elif num_str:
            break
    if num_str:
        return int(num_str)
    return None

def conditions(witness) -> list[bool]:
    try:
        n = 0
        p = None
        
        if isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) >= 2:
                ring = witness[0]
                val = witness[1]
                
                # Handle field of rationals
                if ring == sympy.QQ or str(ring) == 'QQ' or ring == 'Q':
                    try:
                        p = int(val)
                    except Exception:
                        p = extract_number(str(val))
                    if p is not None:
                        h1 = (p == 0)
                        neg_q = True
                        return [bool(h1), bool(neg_q)]
                
                # Extract characteristic/size for Z_n rings
                s = str(ring)
                m = extract_number(s)
                if m is not None:
                    n = m
        else:
            val = witness
            
        if hasattr(val, 'gen'):
            val = val.gen
            
        try:
            p = int(val)
        except Exception:
            s = str(val)
            m = extract_number(s)
            if m is not None:
                p = m
                
        if p is None:
            # Handle polynomial generators like x, y, z
            if str(val) in ['x', 'y', 'z']:
                if n == 2:
                    # In Z2[x], the ideal (x) is prime and the quotient is Z2
                    return [True, False]
                else:
                    # In Z[x] or Q[x], the ideal (x) is prime and the quotient is not Z2
                    return [True, True]
            return [False, False]
            
        if n > 0:
            # In Z_n, the ideal (p) is equivalent to the ideal (gcd(p, n))
            g = gcd(p, n)
            h1 = isprime(g)
            neg_q = g != 2
        else:
            # In Z, the ideal (p) is prime iff |p| is prime or 0
            g = abs(p)
            h1 = isprime(g) or g == 0
            neg_q = g != 2
            
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: R/P is not isomorphic to Z/2Z"
]

N_HYP = 1
NEG_Q_INDEX = 1