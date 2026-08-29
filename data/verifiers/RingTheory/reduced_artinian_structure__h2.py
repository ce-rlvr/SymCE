import sympy
from sympy.ntheory import factorint

# Top-level setup: named object bindings
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, bool):
            pass
        elif isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n >= 2:
                # Z/nZ is a finite ring, hence right Artinian
                h1 = True
                
                # Z/nZ is a direct product of division rings iff n is square-free.
                # (By the Chinese Remainder Theorem, Z/nZ is a product of Z/p^k Z.
                # Z/p^k Z is a division ring iff k=1).
                factors = factorint(n)
                is_square_free = all(v == 1 for v in factors.values())
                neg_q = not is_square_free
                
        elif witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            # Fields are Artinian and are division rings (product of 1 division ring)
            h1 = True
            neg_q = False
            
        elif witness == sympy.S.Integers:
            # Z is not Artinian
            h1 = False
            # Z is not a finite direct product of division rings
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: R is not isomorphic to a finite direct product of division rings"
]

N_HYP = 1
NEG_Q_INDEX = 1