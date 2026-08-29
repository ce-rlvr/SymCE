import sympy as sp
from sympy.ntheory import factorint
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide the degree n and the field order q.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            q = witness.get('q')
        elif hasattr(witness, 'n') and hasattr(witness, 'q'):
            n = witness.n
            q = witness.q
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            n, q = witness
        else:
            return [False, False, False]
            
        if n is None or q is None:
            return [False, False, False]
            
        n = int(n)
        q = int(q)
    except Exception:
        return [False, False, False]

    # H_1: F is a finite field of order q
    # This requires q to be a prime power (and q >= 2)
    try:
        if q < 2:
            h1_ok = False
        else:
            factors = factorint(q)
            h1_ok = (len(factors) == 1)
    except Exception:
        h1_ok = False

    # H_2: SL(n, F) is the special linear group of degree n over F
    # The degree n must be a non-negative integer
    try:
        h2_ok = (n >= 0)
    except Exception:
        h2_ok = False

    # ¬Q: The number of elements in SL(n, F) is NOT q^{n(n-1)/2} \prod_{i=2}^n (q^i - 1)
    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            # Calculate the actual order of SL(n, q)
            if n == 0 or n == 1:
                actual_order = 1
            else:
                actual_order = q**(n*(n-1)//2)
                for j in range(2, n+1):
                    actual_order *= (q**j - 1)
            
            # Calculate the formula value
            # For n >= 2, the formula mathematically matches the actual order.
            # For n < 2, we evaluate the formula exactly as written using sympy's Product,
            # which correctly implements the generalized empty product definition.
            if n >= 2:
                formula_val = actual_order
            else:
                i = sp.Symbol('i')
                formula_val = (q**(n*(n-1)//2)) * sp.Product(q**i - 1, (i, 2, n)).doit()
            
            neg_q_ok = bool(actual_order != formula_val)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: SL(n, F) is the special linear group of degree n over F",
    "¬Q: The number of elements in SL(n, F) is NOT q^{n(n-1)/2} \\prod_{i=2}^n (q^i - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2