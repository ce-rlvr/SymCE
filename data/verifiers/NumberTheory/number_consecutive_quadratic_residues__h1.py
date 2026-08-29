import sympy
from sympy.ntheory import jacobi_symbol

def conditions(witness):
    try:
        p = int(witness)
        # Safeguard against excessively large witnesses to ensure fast execution
        if p > 100000 or p < -100000:
            return [False]
            
        count = 0
        for n in range(1, p - 1):
            if jacobi_symbol(n, p) == 1 and jacobi_symbol(n + 1, p) == 1:
                count += 1
        
        expected = (p - 4 - sympy.S(-1)**sympy.Rational(p - 1, 2)) / 4
        
        neg_q = (count != expected)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The number of consecutive quadratic residues is not (p - 4 - (-1)^((p-1)/2))/4"
]
N_HYP = 0
NEG_Q_INDEX = 0