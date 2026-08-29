import sympy
from sympy import re, eye, zeros
from sympy.ntheory import divisor_sigma

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness object, checks whether it is a valid counterexample to the false conjecture.
    The dropped hypothesis is the definition of sigma(n) as the sum of divisors.
    Thus, the witness must provide a value for s and a function for sigma.
    """
    try:
        # Extract s and sigma from witness
        if isinstance(witness, dict):
            s = witness.get('s', 3)
            sigma = witness.get('sigma', divisor_sigma)
        elif isinstance(witness, tuple) and len(witness) == 2:
            s, sigma = witness
        else:
            s = witness
            sigma = divisor_sigma
            
        # H1: Let the real part of s be strictly greater than 2
        try:
            h1 = bool(re(s) > 2)
        except Exception:
            h1 = False
            
        # H2: Let zeta(s) denote the Riemann zeta function
        # This is a definitional hypothesis, always True in this context
        h2 = True
        
        # ¬Q: The Dirichlet series for sigma(n) does not equal zeta(s)zeta(s-1)
        # We check if sigma(n) matches the true sum of divisors for the first few terms.
        # If it does not match, the Dirichlet series coefficients differ, so the identity fails.
        neg_q = False
        for n in range(1, 20):
            try:
                if hasattr(sigma, '__call__'):
                    val = sigma(n)
                elif hasattr(sigma, 'subs'):
                    val = sigma.subs(sympy.Symbol('n'), n)
                elif isinstance(sigma, (list, tuple, dict)):
                    val = sigma[n]
                else:
                    val = sigma(n)
                    
                if int(val) != divisor_sigma(n):
                    neg_q = True
                    break
            except Exception:
                neg_q = True
                break
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: Let the real part of s be strictly greater than 2",
    "H_2: Let zeta(s) denote the Riemann zeta function",
    "¬Q: sum_{n=1}^{infty} sigma(n)/n^s != zeta(s)zeta(s-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2