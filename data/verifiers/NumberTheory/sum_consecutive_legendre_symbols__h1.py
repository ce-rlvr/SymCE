import sympy
from sympy.ntheory import jacobi_symbol

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that for any integer p, the sum of products of 
    consecutive Legendre symbols from a=1 to p-2 is -1.
    (The true theorem requires p to be an odd prime).
    """
    try:
        # Ensure the witness is an integer
        if isinstance(witness, float) and not witness.is_integer():
            return [False]
        p = int(witness)
        if p != witness:
            return [False]
        # Prevent performance issues with excessively large witnesses
        if abs(p) > 100000:
            return [False]
    except Exception:
        return [False]
        
    try:
        total = 0
        for a in range(1, p - 1):
            # We use jacobi_symbol as the natural generalization of the Legendre symbol
            # for composite numbers. If it raises an error (e.g., for even p), 
            # it will be caught below.
            total += jacobi_symbol(a, p) * jacobi_symbol(a + 1, p)
        neg_q = bool(total != -1)
    except Exception:
        # If the symbol is undefined (e.g., p is even), the sum is undefined,
        # which means it is not equal to -1.
        neg_q = True
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The sum of products of consecutive Legendre symbols is not equal to -1"
]

N_HYP = 0
NEG_Q_INDEX = 0