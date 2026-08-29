import math
import sympy

CONDITION_LABELS = [
    "H_1: A_1 is the arithmetic progression a_1 + n d_1 for n in Z",
    "H_2: A_2 is the arithmetic progression a_2 + n d_2 for n in Z",
    "¬Q: The intersection A_1 ∩ A_2 is NOT a single arithmetic progression with common difference d_1 d_2"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_integer(x):
    return isinstance(x, int) or isinstance(x, sympy.Integer)

def conditions(witness):
    try:
        # Witness should be a tuple (a1, d1, a2, d2)
        if len(witness) != 4:
            return [False, False, False]
        a1, d1, a2, d2 = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = is_integer(a1) and is_integer(d1)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = is_integer(a2) and is_integer(d2)
    except Exception:
        h2_ok = False
        
    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            a1_val, d1_val = int(a1), int(d1)
            a2_val, d2_val = int(a2), int(d2)
            
            g = math.gcd(d1_val, d2_val)
            if g == 0:
                # Both d1 and d2 are 0. The intersection is a single point if a1 == a2, else empty.
                # A single point is an AP with common difference 0, which equals d1 * d2.
                q = (a1_val == a2_val)
            else:
                # If the gcd does not divide the difference of the starting points, the intersection is empty.
                # An empty set is not a single arithmetic progression.
                if (a1_val - a2_val) % g != 0:
                    q = False
                else:
                    # The intersection is non-empty and forms an AP with common difference lcm(d1, d2).
                    # We check if this common difference equals |d1 * d2|.
                    lcm_val = abs(d1_val * d2_val) // g
                    q = (lcm_val == abs(d1_val * d2_val))
                    
            neg_q_ok = not q
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]