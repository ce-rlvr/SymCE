import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple (n, S, m) where:
      - n is an integer >= 2, representing the commutative ring R = Z/nZ.
      - S is a list/set of integers, representing a subset of R.
      - m is an integer >= 1 dividing n, representing the R-module M = Z/mZ.
    """
    try:
        n, S, m = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring and M is an R-module
    try:
        h1 = isinstance(n, int) and n >= 2 and isinstance(m, int) and m >= 1 and n % m == 0
    except Exception:
        h1 = False
        
    # H_2: S is a multiplicatively closed subset of R
    try:
        if not isinstance(S, (list, tuple, set)):
            h2 = False
        else:
            S_set = set(S)
            if len(S_set) == 0:
                h2 = False
            elif not all(isinstance(x, int) and 0 <= x < n for x in S_set):
                h2 = False
            else:
                h2 = True
                for a in S_set:
                    for b in S_set:
                        if (a * b) % n not in S_set:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    # ¬Q: S^{-1}M is neither the zero module nor a simple S^{-1}R-module
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # Calculate the size of the submodule I_M of elements annihilated by S
            I_M_size = 0
            for i in range(m):
                for s in S_set:
                    if (s * i) % m == 0:
                        I_M_size += 1
                        break
            
            # S^{-1}M is isomorphic to M / I_M. 
            # Since M = Z/mZ, M / I_M is a cyclic group of order g = m / |I_M|.
            g = m // I_M_size
            
            # The submodules of S^{-1}M correspond to the subgroups of this cyclic group,
            # which are in bijection with the divisors of g.
            divisors = 0
            for i in range(1, g + 1):
                if g % i == 0:
                    divisors += 1
            
            # The module is zero if it has 1 submodule (divisors == 1).
            # The module is simple if it has exactly 2 submodules (divisors == 2).
            # The conclusion fails if it has > 2 submodules.
            neg_q = divisors > 2
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring and M is an R-module",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}M is neither the zero module nor a simple S^{-1}R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2