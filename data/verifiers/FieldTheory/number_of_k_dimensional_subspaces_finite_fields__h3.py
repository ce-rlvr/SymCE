import sympy
import sympy.ntheory
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        q, n, k = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F_q is a finite field with q elements
    try:
        if isinstance(q, (int, sympy.Integer)) and q >= 2:
            factors = sympy.ntheory.factorint(int(q))
            h1 = (len(factors) == 1)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: V is an n-dimensional vector space over F_q
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and n >= 0
    except Exception:
        h2 = False
        
    # ¬Q: The number of distinct k-dimensional subspaces is not equal to the formula
    try:
        if not isinstance(k, (int, sympy.Integer)):
            neg_q = False
        else:
            k_int = int(k)
            n_int = int(n)
            q_int = int(q)
            
            # Calculate the actual number of k-dimensional subspaces
            if k_int < 0 or k_int > n_int:
                actual = 0
            else:
                num = 1
                den = 1
                for i in range(k_int):
                    num *= (q_int**n_int - q_int**i)
                    den *= (q_int**k_int - q_int**i)
                actual = num // den
                
            # Calculate the formula value
            # \prod_{i=0}^{k-1} \frac{q^n - q^i}{q^k - q^i}
            # If k <= 0, the product is empty and evaluates to 1.
            if k_int <= 0:
                formula_val = 1
            else:
                formula_val = 1
                for i in range(k_int):
                    formula_val *= sympy.Rational(q_int**n_int - q_int**i, q_int**k_int - q_int**i)
                    
            neg_q = bool(actual != formula_val)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: V is an n-dimensional vector space over F_q",
    "¬Q: The number of distinct k-dimensional subspaces is not equal to the formula"
]

N_HYP = 2
NEG_Q_INDEX = 2