import sympy
from sympy.ntheory import divisor_sigma

CONDITION_LABELS = [
    "¬Q: sigma(10^k) != (2^{k+1}-1)(5^{k+1}-1)/4"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        k = sympy.sympify(witness)
        if not k.is_number:
            return [False]
            
        rhs = ((2**(k+1) - 1) * (5**(k+1) - 1)) / 4
        
        val = 10**k
        
        try:
            # Check if 10^k is mathematically an integer
            if val == int(val):
                lhs = divisor_sigma(int(val))
                neg_q = bool(lhs != rhs)
            else:
                # If 10^k is not an integer, the standard divisor_sigma is undefined,
                # so the equality fails.
                neg_q = True
        except (TypeError, ValueError, OverflowError):
            # Catch cases where int(val) fails (e.g., complex numbers, infinities)
            # or divisor_sigma raises an error.
            neg_q = True
            
    except Exception:
        neg_q = False

    return [neg_q]