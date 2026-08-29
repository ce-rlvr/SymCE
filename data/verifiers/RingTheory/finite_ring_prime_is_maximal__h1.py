import sympy
from sympy import isprime, symbols
import math
from functools import reduce

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let P be a prime ideal of R. Then P is a maximal ideal of R."
    
    A valid witness could be an integer `n` (representing the ideal nZ in Z),
    or a tuple `(ring, generators)`.
    """
    h1_ok = False
    neg_q_ok = False
    
    try:
        ring = None
        gens = []
        
        # Parse the witness
        if isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer):
            ring = 'ZZ'
            gens = [abs(int(witness))]
        elif isinstance(witness, tuple) and len(witness) == 2:
            ring, P = witness
            if isinstance(P, (list, tuple, set)):
                gens = list(P)
            else:
                gens = [P]
        elif isinstance(witness, (list, tuple, set)):
            ring = 'ZZ'
            gens = list(witness)
        else:
            ring = 'ZZ'
            gens = [witness]

        # Evaluate conditions based on the ring
        if ring in ('ZZ', sympy.ZZ, 'Z'):
            if len(gens) == 0:
                n = 0
            else:
                n = reduce(math.gcd, [abs(int(g)) for g in gens])
            
            # In Z, an ideal (n) is prime if n == 0 or n is prime.
            h1_ok = (n == 0 or isprime(n))
            # In Z, an ideal (n) is maximal if and only if n is prime.
            is_maximal = isprime(n)
            neg_q_ok = not is_maximal
            
        elif str(ring) in ('ZZ[x]', 'Z[x]'):
            gens_str = sorted([str(g) for g in gens])
            # (0), (x), and (p) are prime but not maximal in Z[x]
            if gens_str in [['x'], ['0'], ['2'], ['3'], ['5'], ['7']]:
                h1_ok = True
                neg_q_ok = True
            # (p, x) are maximal in Z[x]
            elif gens_str in [['2', 'x'], ['3', 'x'], ['5', 'x']]:
                h1_ok = True
                neg_q_ok = False
                
        elif str(ring) in ('QQ[x]', 'Q[x]'):
            gens_str = sorted([str(g) for g in gens])
            # (0) is prime but not maximal in Q[x]
            if gens_str == ['0']:
                h1_ok = True
                neg_q_ok = True
            # (x) is maximal in Q[x]
            elif gens_str == ['x']:
                h1_ok = True
                neg_q_ok = False
                
        elif str(ring) in ('QQ[x,y]', 'Q[x,y]', 'QQ[x, y]'):
            gens_str = sorted([str(g) for g in gens])
            # (x) and (y) are prime but not maximal in Q[x,y]
            if gens_str in [['x'], ['y']]:
                h1_ok = True
                neg_q_ok = True
                
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1