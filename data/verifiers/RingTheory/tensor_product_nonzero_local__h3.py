import sympy
from sympy import QQ
from sympy.ntheory import factorint
import math

# Top-level setup for potential witness expressions
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z7 = 7
Z8 = 8
Z9 = 9

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "If R is a commutative local ring, M and N are finitely generated R-modules,
    and N is not the zero module, then M \otimes_R N is not the zero module."
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', witness.get('n'))
            M = witness['M']
            N = witness['N']
        else:
            R, M, N = witness
    except Exception:
        return [False, False, False, False]

    h1 = False
    h2 = False
    h3 = False
    neg_q = False

    # Case 1: R is a field (e.g., QQ), which is a local ring.
    # M and N are represented by their vector space dimensions (non-negative integers).
    try:
        is_field = False
        if R == QQ or str(R) == 'QQ':
            is_field = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            is_field = True
            
        if is_field:
            h1 = True
            if isinstance(M, (int, sympy.Integer)) and int(M) >= 0 and isinstance(N, (int, sympy.Integer)) and int(N) >= 0:
                h2 = True
                h3 = (int(N) > 0)
                neg_q = (int(M) * int(N) == 0)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Case 2: R is Z/nZ represented by an integer n >= 2.
    # M and N are lists of integers d_i dividing n, representing \bigoplus Z/d_i Z.
    try:
        if isinstance(R, (int, sympy.Integer)) and int(R) >= 2:
            R_int = int(R)
            # Z/nZ is a local ring iff n is a prime power
            factors = factorint(R_int)
            if len(factors) == 1:
                h1 = True
                
            if isinstance(M, (int, sympy.Integer)) and int(M) == 0:
                M_list = []
            elif isinstance(M, (int, sympy.Integer)):
                M_list = [int(M)]
            else:
                M_list = list(M)
                
            if isinstance(N, (int, sympy.Integer)) and int(N) == 0:
                N_list = []
            elif isinstance(N, (int, sympy.Integer)):
                N_list = [int(N)]
            else:
                N_list = list(N)
                
            # Finitely generated R-modules must be annihilated by R_int
            h2_M = all(isinstance(m, (int, sympy.Integer)) and int(m) != 0 and R_int % int(m) == 0 for m in M_list)
            h2_N = all(isinstance(n_, (int, sympy.Integer)) and int(n_) != 0 and R_int % int(n_) == 0 for n_ in N_list)
            if h2_M and h2_N:
                h2 = True
                
            # N is not the zero module iff it has a component Z/dZ with d > 1
            h3 = any(abs(int(n_)) > 1 for n_ in N_list)
            
            # M \otimes_R N is the zero module iff gcd(m, n_) == 1 for all components
            neg_q = all(math.gcd(int(m), int(n_)) == 1 for m in M_list for n_ in N_list)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring",
    "H_2: M and N are finitely generated R-modules",
    "H_3: N is not the zero module",
    "¬Q: M \\otimes_R N is the zero module"
]

N_HYP = 3
NEG_Q_INDEX = 3