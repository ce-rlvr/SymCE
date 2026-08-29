import sympy
from sympy import ZZ
import math

# Top-level setup for standard rings
Z = ZZ

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, I, J, n) or (I, J, n) assuming R=Z.
    For R=Z, ideals I and J can be given as integers (generators) or lists of integers.
    """
    try:
        if len(witness) == 4:
            R, I, J, n = witness
        elif len(witness) == 3:
            R = ZZ
            I, J, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring
    try:
        # We support Z as the primary commutative ring for counterexamples
        h1 = R in ("Z", ZZ, sympy.S.Integers, "ZZ")
    except Exception:
        h1 = False
        
    # H_2: n is a non-negative integer
    try:
        h2 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n >= 0
    except Exception:
        h2 = False
        
    # ¬Q: Tor_n^R(R/I, R/J) is not the zero module
    try:
        if not h1:
            neg_q = False
        else:
            def get_gen(ideal):
                if isinstance(ideal, (int, sympy.Integer)):
                    return int(ideal)
                if isinstance(ideal, (list, tuple, set)):
                    g = 0
                    for x in ideal:
                        g = math.gcd(g, int(x))
                    return g
                try:
                    return int(ideal)
                except Exception:
                    if hasattr(ideal, 'as_coeff_Mul'):
                        coeff, _ = ideal.as_coeff_Mul()
                        return int(coeff)
                    return 1
            
            a = get_gen(I)
            b = get_gen(J)
            
            g = math.gcd(a, b)
            
            if n == 0:
                # Tor_0(Z/aZ, Z/bZ) = Z/gcd(a,b)Z. Zero module iff gcd(a,b) == 1.
                neg_q = (abs(g) != 1)
            elif n == 1:
                # Tor_1(Z/aZ, Z/bZ) = Z/gcd(a,b)Z if a != 0 and b != 0.
                # If a = 0 or b = 0, Tor_1 is 0.
                if a == 0 or b == 0:
                    neg_q = False
                else:
                    neg_q = (abs(g) != 1)
            else:
                # For Z, global dimension is 1, so Tor_n is 0 for n >= 2.
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is a non-negative integer",
    "¬Q: Tor_n^R(R/I, R/J) is not the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2