import math
import sympy

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is the integer d.
    """
    try:
        # H_1: d is an integer
        h1 = (isinstance(witness, int) or isinstance(witness, sympy.Integer)) and not isinstance(witness, bool)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            d = int(witness)
            
            # The conclusion states that Z[x]/(x^2 - d) is isomorphic to the ring of 
            # algebraic integers of Q(sqrt(d)).
            # This is true if and only if d is square-free and d ≡ 2 or 3 (mod 4).
            # If d is a perfect square, Q(sqrt(d)) = Q, whose ring of integers is Z,
            # which is not isomorphic to Z[x]/(x^2 - d) (rank 1 vs rank 2 over Z).
            
            if d >= 0 and math.isqrt(d)**2 == d:
                neg_q = True
            else:
                is_sq_free = True
                if d == 0:
                    is_sq_free = False
                else:
                    abs_d = abs(d)
                    for i in range(2, math.isqrt(abs_d) + 1):
                        if abs_d % (i * i) == 0:
                            is_sq_free = False
                            break
                
                if not is_sq_free:
                    neg_q = True
                elif d % 4 == 1:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: d is an integer",
    "¬Q: R/I is not isomorphic to the ring of algebraic integers of Q(sqrt(d))"
]

N_HYP = 1
NEG_Q_INDEX = 1