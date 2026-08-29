import sympy
from sympy import Integer, S, QQ, ZZ
from sympy.ntheory import factorint

# Top-level setup
# Integers are used directly to represent the finite rings Z/nZ.
# Standard infinite rings/fields are also available.

def is_square_free(n):
    factors = factorint(n)
    return all(exp == 1 for exp in factors.values())

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the conjecture:
    "Every commutative Artinian ring with identity is isomorphic to a finite direct product of fields."
    
    The witness can be:
      - An integer n >= 2, representing the ring Z/nZ.
      - A list/tuple of integers n_i >= 2, representing the direct product of Z/n_i Z.
      - A standard SymPy ring/field like ZZ, QQ, S.Reals, etc.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Handle standard SymPy domains/sets
        if witness in (S.Reals, S.Complexes, S.Rationals, QQ):
            # Fields are commutative Artinian rings and are trivially a product of (one) field.
            return [True, True, False]
        if witness in (S.Integers, ZZ):
            # The integers form a commutative ring with identity, but it is not Artinian.
            return [True, False, True]
            
        # Handle integer witness representing Z/nZ
        if isinstance(witness, (int, Integer)):
            n = int(witness)
            if n >= 2:
                h1 = True  # Z/nZ is a commutative ring with identity
                h2 = True  # Finite rings are Artinian
                # Z/nZ is a finite direct product of fields iff n is square-free
                neg_q = not is_square_free(n)
                
        # Handle tuple/list of integers representing a direct product of Z/n_i Z
        elif isinstance(witness, (list, tuple)):
            if all(isinstance(x, (int, Integer)) for x in witness):
                rings = [int(x) for x in witness]
                if rings and all(n >= 2 for n in rings):
                    h1 = True
                    h2 = True
                    # A direct product of Z/n_i Z is a product of fields iff all n_i are square-free
                    neg_q = any(not is_square_free(n) for n in rings)
                    
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is an Artinian ring",
    "¬Q: R is not isomorphic to a finite direct product of fields"
]

N_HYP = 2
NEG_Q_INDEX = 2