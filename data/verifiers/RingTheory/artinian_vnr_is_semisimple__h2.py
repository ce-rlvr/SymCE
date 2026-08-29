import sympy
from sympy.ntheory import factorint
from sympy.polys.domains import ZZ, QQ

# Top-level setup: named object bindings that the witness expression may reference.
# We interpret an integer n >= 2 as the ring Z/nZ.
Z2 = 2
Z3 = 3
Z4 = 4
Z6 = 6
Z8 = 8
Z9 = 9
Z12 = 12

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "Every right Artinian ring is semisimple."
    
    We primarily interpret an integer n >= 2 as the finite ring Z/nZ.
    """
    h1 = False
    neg_q = False
    
    def is_square_free(n):
        if n == 0:
            return False
        factors = factorint(abs(n))
        return all(exp == 1 for exp in factors.values())
    
    try:
        # Integer n represents the ring Z/nZ
        if isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            n = int(witness)
            if n >= 2:
                h1 = True  # Z/nZ is finite, hence right Artinian
                neg_q = not is_square_free(n)  # Z/nZ is semisimple iff n is square-free
                
        # Tuple (ZZ, n) represents Z/nZ
        elif isinstance(witness, tuple) and len(witness) == 2 and witness[0] == ZZ:
            n = int(witness[1])
            if n >= 2:
                h1 = True
                neg_q = not is_square_free(n)
                
        # Sympy QuotientRing over ZZ
        elif hasattr(witness, 'base_ring') and witness.base_ring == ZZ:
            if hasattr(witness, 'base_ideal'):
                gen = witness.base_ideal.gens[0]
            elif hasattr(witness, 'ideal'):
                gen = witness.ideal.gens[0]
            else:
                gen = 0
            n = abs(int(gen))
            if n >= 2:
                h1 = True
                neg_q = not is_square_free(n)
                
        # The ring of integers ZZ
        elif witness == ZZ:
            h1 = False  # ZZ is not Artinian
            neg_q = True  # ZZ is not semisimple
            
        # The field of rationals QQ
        elif witness == QQ:
            h1 = True  # Fields are Artinian
            neg_q = False  # Fields are semisimple
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: R is not a semisimple ring"
]

N_HYP = 1
NEG_Q_INDEX = 1