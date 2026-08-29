import sympy
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        h1 = False
        neg_q = False
        
        # Case 1: Witness is an integer, implicitly in the ring Z.
        # In Z, idempotents are {0, 1} and units are {1, -1}.
        # Thus, eu can only be 0, 1, or -1.
        if isinstance(witness, (int, sympy.Integer)):
            h1 = True
            neg_q = witness not in [0, 1, -1]
            
        # Case 2: Witness is a tuple (a, n), representing element a in the ring Z_n.
        elif isinstance(witness, tuple) and len(witness) == 2:
            a, n = witness
            if isinstance(a, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and n > 1:
                h1 = True
                a = int(a) % int(n)
                n = int(n)
                
                idempotents = [e for e in range(n) if (e * e) % n == e]
                units = [u for u in range(n) if math.gcd(u, n) == 1]
                
                can_be_written = False
                for e in idempotents:
                    for u in units:
                        if (e * u) % n == a:
                            can_be_written = True
                            break
                    if can_be_written:
                        break
                neg_q = not can_be_written
                
        # Case 3: Witness is a matrix.
        # Matrices over fields are unit-regular (can always be written as EU).
        # Without knowing the exact base ring intended, we safely assume it might be over a field.
        elif isinstance(witness, sympy.Matrix):
            h1 = True
            neg_q = False
            
        # Case 4: Witness is a float (implicitly in the field R).
        # Fields are unit-regular.
        elif isinstance(witness, float):
            h1 = True
            neg_q = False
            
        # Case 5: Witness is a sympy expression (e.g., polynomials or constants).
        elif isinstance(witness, sympy.Expr):
            h1 = True
            if witness.free_symbols:
                # Non-constant polynomials over domains cannot be written as eu
                # because idempotents are constants {0, 1} and units are constants.
                neg_q = True
            else:
                if witness.is_Integer:
                    val = int(witness)
                    neg_q = val not in [0, 1, -1]
                else:
                    # Rational or real constants belong to fields, which are unit-regular.
                    neg_q = False
                    
    except Exception:
        h1 = False
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an element of a ring",
    "¬Q: a cannot be written as eu for idempotent e and unit u"
]

N_HYP = 1
NEG_Q_INDEX = 1