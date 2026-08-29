import math
import sympy

# Top-level setup for common rings Z_n
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness):
    try:
        # If witness is just an integer, treat it as the ring Z_n
        # and check if there exists ANY principal ideal that is not projective.
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n < 2:
                return [False, False]
            h1_ok = True
            # In Z_n, there exists a non-projective principal ideal iff n is not square-free.
            neg_q_ok = not sympy.is_squarefree(n)
            return [h1_ok, neg_q_ok]

        # Otherwise, expect a tuple (n, a) representing Z_n and generator a
        n, a = None, None
        if isinstance(witness, tuple) and len(witness) == 2:
            n, a = witness
        elif isinstance(witness, dict) and 'n' in witness and 'a' in witness:
            n, a = witness['n'], witness['a']
        elif hasattr(witness, 'n') and hasattr(witness, 'a'):
            n, a = witness.n, witness.a
            
        if isinstance(a, (list, tuple, set)) and len(a) == 1:
            a = list(a)[0]
            
        if n is None or a is None:
            return [False, False]
            
        n = int(n)
        a = int(a)
        
        if n < 2:
            return [False, False]
            
        h1_ok = True
        
        # In Z_n, the principal ideal (a) is projective iff gcd(a, n) and n / gcd(a, n) are coprime.
        g = math.gcd(a, n)
        comp = n // g
        neg_q_ok = math.gcd(g, comp) != 1
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is a principal ideal of R",
    "¬Q: I is not a projective R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1