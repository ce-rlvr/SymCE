import sympy
import math
from itertools import combinations
from sympy.abc import x, y, z
from sympy import Rational, Integer
from sympy.matrices import eye, zeros

# Standard algebra objects for RingTheory / Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the "pairwise coprime" hypothesis from the Chinese Remainder Theorem,
    and claims the kernel of the natural map is the intersection.
    Mathematically, the kernel is ALWAYS the intersection. However, in the context of the CRT,
    dropping the coprime hypothesis causes the isomorphism to fail (f is not surjective, 
    and intersection != product). We evaluate the intended failure by checking if the ideals 
    are NOT pairwise coprime.
    """
    try:
        # Parse the witness to extract the list of ideals
        if not isinstance(witness, (list, tuple)):
            return [False, False, False]
            
        if isinstance(witness, tuple) and len(witness) >= 2:
            # Handle cases like (Ring, [I_1, I_2]) or (Ring, I_1, I_2)
            if isinstance(witness[1], (list, tuple)):
                ideals = witness[1]
            elif not isinstance(witness[0], (int, sympy.Expr)):
                ideals = witness[1:]
            else:
                ideals = witness
        else:
            ideals = witness
            
        if not isinstance(ideals, (list, tuple)) or len(ideals) < 2:
            return [False, False, False]
            
        # H1: R is a ring (implicitly true for Z or K[x] based on valid ideal inputs)
        h1 = True
        
        # H2: f is the ring homomorphism defined by f(x) = (x + I_1, ..., x + I_n)
        h2 = True
        
        # ¬Q: The intended CRT conclusion fails.
        # This happens exactly when the ideals are NOT pairwise coprime.
        is_pairwise_coprime = True
        for a, b in combinations(ideals, 2):
            g = sympy.gcd(a, b)
            if isinstance(g, (int, sympy.Integer)):
                if abs(int(g)) != 1:
                    is_pairwise_coprime = False
                    break
            else:
                # For polynomial ideals
                if not g.is_constant():
                    is_pairwise_coprime = False
                    break
                    
        neg_q = not is_pairwise_coprime
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: f is the ring homomorphism defined by f(x) = (x + I_1, ..., x + I_n)",
    "¬Q: The intended CRT conclusion fails (ideals are not pairwise coprime)"
]

N_HYP = 2
NEG_Q_INDEX = 2