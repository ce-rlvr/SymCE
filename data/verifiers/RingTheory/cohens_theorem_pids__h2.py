import sympy
from sympy import isprime

# Top-level setup: named object bindings
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Every prime ideal of R is a principal ideal",
    "¬Q: R is not a principal ideal domain"
]

def conditions(witness):
    try:
        if witness == sympy.S.Integers:
            return [True, True, False]
        if witness == sympy.S.Rationals:
            return [True, True, False]
            
        if isinstance(witness, str):
            s = witness.strip().replace(' ', '').lower()
            if s in ['z', 'zz']:
                return [True, True, False]
            if s in ['q', 'qq']:
                return [True, True, False]
            if s in ['z[x]', 'zz[x]']:
                return [True, False, True]
            if s in ['q[x]', 'qq[x]']:
                return [True, True, False]
            if s in ['q[x,y]', 'qq[x,y]']:
                return [True, False, True]
            if s in ['z[i]', 'zz[i]']:
                return [True, True, False]
            if s in ['q[x]/(x^2)', 'qq[x]/(x^2)', 'r[x]/(x^2)', 'c[x]/(x^2)']:
                return [True, True, True]
                
        if isinstance(witness, tuple) and len(witness) > 1:
            if all(isinstance(x, int) for x in witness):
                if all(x > 1 for x in witness):
                    return [True, True, True]
                else:
                    return [False, False, False]

        n = None
        if isinstance(witness, int):
            n = witness
        elif hasattr(witness, 'is_Integer') and witness.is_Integer:
            n = int(witness)
        elif isinstance(witness, str):
            s = witness.strip().replace(' ', '').lower()
            if s.startswith('z/') and s.endswith('z'):
                try:
                    n = int(s[2:-1])
                except ValueError:
                    pass
            elif s.startswith('z_'):
                try:
                    n = int(s[2:])
                except ValueError:
                    pass
            else:
                try:
                    n = int(s)
                except ValueError:
                    pass
                    
        if n is not None:
            if n <= 1:
                return [False, False, False]
            
            # H1: R is a commutative ring
            # Z/nZ is always a commutative ring for n > 1
            h1 = True
            
            # H2: Every prime ideal of R is a principal ideal
            # In Z/nZ, every ideal is principal, so every prime ideal is principal.
            h2 = True
            
            # neg_Q: R is not a principal ideal domain
            # Z/nZ is a PID iff n is prime.
            neg_q = not isprime(n)
            
            return [h1, h2, neg_q]
            
    except Exception:
        pass

    return [False, False, False]