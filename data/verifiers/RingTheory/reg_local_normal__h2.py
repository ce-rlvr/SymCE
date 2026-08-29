import sympy
from sympy import isprime
from sympy.polys.domains import Domain

# Top-level setup: named object bindings
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals
RR = sympy.S.Reals
CC = sympy.S.Complexes

# Integer witnesses are interpreted as the ring Z/nZ
Z2 = 2
Z3 = 3
Z4 = 4
Z6 = 6

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # If witness is an integer n, we interpret it as the ring Z/nZ
        if isinstance(witness, (int, sympy.Integer)):
            n = abs(int(witness))
            if n >= 1:
                h1 = True
                # Z/nZ is a domain iff n is prime.
                # If it is not a domain, it cannot be an integrally closed domain.
                neg_q = not isprime(n)
            elif n == 0:
                # Z/0Z is isomorphic to Z, which is an integrally closed domain
                h1 = True
                neg_q = False
                
        # If witness is a SymPy Domain
        elif isinstance(witness, Domain):
            h1 = True
            # SymPy domains (ZZ, QQ, RR, CC, polynomial rings, fraction fields)
            # are all integral domains, and the standard ones are integrally closed.
            neg_q = False
            
        # If witness is a SymPy Set like S.Integers
        elif witness in (ZZ, QQ, RR, CC):
            h1 = True
            neg_q = False
            
        # If witness is a string like "Z/4Z"
        elif isinstance(witness, str):
            s = witness.replace(" ", "")
            if s.startswith("Z/") and s.endswith("Z"):
                n_str = s[2:-1]
                if n_str.isdigit():
                    n = int(n_str)
                    if n >= 1:
                        h1 = True
                        neg_q = not isprime(n)
                        
        # If witness is a tuple like (ZZ, 4) representing Z/4Z
        elif isinstance(witness, tuple) and len(witness) == 2:
            if witness[0] in (ZZ, sympy.polys.domains.ZZ) and isinstance(witness[1], (int, sympy.Integer)):
                n = abs(int(witness[1]))
                if n >= 1:
                    h1 = True
                    neg_q = not isprime(n)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: R is not an integrally closed domain"
]

N_HYP = 1
NEG_Q_INDEX = 1