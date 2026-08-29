import sympy
import math

# Top-level setup
# No specific named bindings needed for this number theory conjecture.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be an integer n (or a tuple starting with n).
    """
    try:
        if isinstance(witness, (tuple, list)):
            n_val = witness[0]
        else:
            n_val = witness
            
        if isinstance(n_val, int):
            n = n_val
            h1 = True
        elif hasattr(n_val, 'is_integer') and n_val.is_integer:
            n = int(n_val)
            h1 = True
        else:
            h1 = False
            n = None
    except Exception:
        h1 = False
        n = None

    neg_q = False
    if h1 and n is not None:
        try:
            # Evaluate c_n(n) based on the sum definition:
            # sum_{k=1, gcd(k,n)=1}^n e^{2*pi*i*k*n/n} = sum_{k=1, gcd(k,n)=1}^n 1
            if n >= 1:
                c_n = sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)
            else:
                # For n < 1, the sum from 1 to n is empty
                c_n = 0
            
            # Evaluate phi(n)
            if n == 0:
                phi_n = 0
            else:
                phi_n = sympy.totient(abs(n))
                
            # The conclusion is c_n(n) == phi(n). We want its negation.
            if c_n != phi_n:
                neg_q = True
        except Exception:
            neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: c_n(m) is the Ramanujan sum",
    "¬Q: c_n(n) != phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1