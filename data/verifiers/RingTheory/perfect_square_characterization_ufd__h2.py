import sympy
import math

# Top-level setup
Z = sympy.S.Integers

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "In a UFD R, a is a perfect square iff every prime factor in its unique 
    prime factorization appears with an even exponent."
    
    The witness can be an integer `a` (implicitly in Z) or a tuple `(Z, a)`.
    """
    # H_1: R is a Unique Factorization Domain
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, a = witness
            h1 = (R == Z or R == 'Z') and isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool)
        else:
            a = witness
            h1 = isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool)
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails at the witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            _, a = witness
        else:
            a = witness
            
        a_val = int(a)
        
        # 0 is a perfect square but its prime factorization is undefined/degenerate.
        # We only consider non-zero elements for standard UFD prime factorization.
        if a_val == 0:
            neg_q = False
        else:
            # Check if a is a perfect square in Z
            is_perfect_square = (a_val >= 0) and (math.isqrt(a_val)**2 == a_val)
            
            # Check if every prime factor has an even exponent
            # abs(a_val) correctly ignores the unit -1 in Z
            factors = sympy.factorint(abs(a_val))
            all_even = all(exp % 2 == 0 for p, exp in factors.items())
            
            # The conclusion is that these two conditions are equivalent
            conclusion = (is_perfect_square == all_even)
            
            # We want the conclusion to FAIL
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: It is not true that a is a perfect square iff every prime factor has an even exponent"
]

N_HYP = 1
NEG_Q_INDEX = 1