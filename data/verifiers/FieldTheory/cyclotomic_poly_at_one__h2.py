import sympy
from sympy import factorint
from sympy.polys import cyclotomic_poly
from sympy.abc import x

# Top-level setup
# (No specific named objects needed for this number theory problem; integers are used directly)

def conditions(witness):
    # H_1: n > 1 is an integer
    try:
        if isinstance(witness, bool):
            h1 = False
        else:
            n = int(witness)
            h1 = (n > 1) and (n == witness)
    except Exception:
        h1 = False

    # neg_Q: conclusion fails
    try:
        n = int(witness)
        
        # Evaluate the n-th cyclotomic polynomial at x = 1
        poly = cyclotomic_poly(n, x)
        val = poly.subs(x, 1)
        
        # Find prime factors of n
        factors = factorint(n)
        # Filter out 1 or -1 just in case of unexpected inputs
        factors = {k: v for k, v in factors.items() if k > 1}
        
        q_holds = True
        if len(factors) == 1:
            # n is a power of a single prime p
            p = list(factors.keys())[0]
            if int(val) != p:
                q_holds = False
        elif len(factors) >= 2:
            # n is divisible by at least two distinct primes
            if int(val) != 1:
                q_holds = False
                
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n > 1 is an integer",
    "¬Q: Phi_n(1) != p for prime power n, or Phi_n(1) != 1 for n with >= 2 distinct prime factors"
]

N_HYP = 1
NEG_Q_INDEX = 1