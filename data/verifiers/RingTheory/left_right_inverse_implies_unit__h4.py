import sympy
from sympy import eye, zeros

# Standard linear algebra objects that might be used in a witness
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring with identity 1",
    "H_2: a is an element of R",
    "H_3: There exists an element b in R such that ba = 1",
    "¬Q: a is not a unit in R or b != c"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        c = None
        if isinstance(witness, tuple):
            if len(witness) == 2:
                a, b = witness
                one = b * a
            elif len(witness) == 3:
                a, b, one = witness
            elif len(witness) == 4:
                a, b, c, one = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        # H_1: R is a ring with identity 1
        # We verify that 'one' acts as a multiplicative identity for the provided elements
        # and that the elements can be multiplied in both directions.
        try:
            _ = a * b
            h1 = bool((one * a == a) and (a * one == a) and 
                      (one * b == b) and (b * one == b) and 
                      (one * one == one))
        except Exception:
            h1 = False
            
        # H_2: a is an element of R
        try:
            h2 = (a is not None)
        except Exception:
            h2 = False
            
        # H_3: There exists an element b in R such that ba = 1
        try:
            h3 = bool(b * a == one)
        except Exception:
            h3 = False
            
        # ¬Q: a is not a unit in R or b != c
        # a is a unit if and only if it has a two-sided inverse.
        # Since ba = 1, a is a unit iff ab = 1.
        try:
            a_is_unit = bool(a * b == one)
            if c is not None:
                conclusion = a_is_unit and bool(b == c)
            else:
                # If c is not provided, the conclusion can only hold if a is a unit.
                conclusion = a_is_unit
            neg_q = not conclusion
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]