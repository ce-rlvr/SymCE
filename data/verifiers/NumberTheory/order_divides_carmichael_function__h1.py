import sympy
import math

from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should provide an integer `a` and an integer `n`.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            n = witness.get('n')
        else:
            a, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: a is an integer coprime to n
    try:
        a_int = int(a)
        n_int = int(n)
        # Ensure they are exactly integers (reject floats like 2.5)
        h1 = (a_int == a) and (n_int == n) and (math.gcd(a_int, n_int) == 1)
    except Exception:
        h1 = False
        
    # H_2: \lambda(n) denotes the Carmichael function of n
    # This is a definitional hypothesis, so it holds trivially in our evaluation context.
    h2 = True
    
    # ¬Q: The order of a modulo n does NOT divide \lambda(n)
    try:
        if not h1:
            neg_q = False
        else:
            a_int = int(a)
            n_int = int(n)
            
            # The Carmichael function and multiplicative order are strictly defined for n > 0.
            # If n <= 0, the conclusion is undefined/fails.
            if n_int <= 0:
                neg_q = True
            else:
                k = sympy.n_order(a_int, n_int)
                l = sympy.reduced_totient(n_int)
                neg_q = (l % k != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer coprime to n",
    "H_2: \\lambda(n) denotes the Carmichael function of n",
    "¬Q: The order of a modulo n does not divide \\lambda(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2