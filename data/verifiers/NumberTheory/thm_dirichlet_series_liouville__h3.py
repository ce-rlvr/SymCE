import sympy as sp

# Top-level setup
# (No specific named objects required for this NumberTheory problem)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it FAILS the conclusion (neg_Q).
    
    The witness is expected to be the complex number s, 
    or a tuple (s, lam) where lam is a function representing lambda(n).
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        s, lam = witness
    else:
        s = witness
        # Default to the Liouville function if not explicitly provided
        lam = lambda n: (-1)**sp.primeomega(n)
        
    # H_1: s is a complex number with Re(s) > 1
    try:
        s_c = complex(s)
        h1 = bool(s_c.real > 1.0)
    except Exception:
        h1 = False
        
    # H_2: lambda(n) is the Liouville function
    try:
        # Verify the function matches the Liouville function for the first 100 integers
        h2 = all(lam(n) == (-1)**sp.primeomega(n) for n in range(1, 101))
    except Exception:
        h2 = False
        
    # ¬Q: The Dirichlet series does NOT converge absolutely to zeta(2s)/zeta(s)
    try:
        if not h1:
            # If Re(s) <= 1, the series sum |lam(n)/n^s| = sum 1/n^Re(s) diverges,
            # so it does not converge absolutely.
            neg_q = True
        elif not h2:
            # If lam is not the Liouville function, it generally won't converge to zeta(2s)/zeta(s).
            neg_q = True
        else:
            # If Re(s) > 1 and lam is the Liouville function, it mathematically converges 
            # absolutely to exactly zeta(2s)/zeta(s). Thus, the conclusion holds, so its negation is False.
            neg_q = False
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: s is a complex number with Re(s) > 1",
    "H_2: lambda(n) is the Liouville function",
    "¬Q: The Dirichlet series does not converge absolutely to zeta(2s)/zeta(s)"
]

N_HYP = 2
NEG_Q_INDEX = 2