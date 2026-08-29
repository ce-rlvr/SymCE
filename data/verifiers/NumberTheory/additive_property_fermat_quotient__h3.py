import sympy
import math

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        p, a, b = witness
    except Exception:
        return [False, False, False]
        
    try:
        p_int = int(p)
        h1 = sympy.isprime(p_int) and p_int % 2 != 0 and p_int == p
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)) and not isinstance(a, bool) and not isinstance(b, bool)
    except Exception:
        h2 = False
        
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            p_int = int(p)
            a_int = int(a)
            b_int = int(b)
            
            num = (a_int**(p_int - 1) - 1) * (b_int**(p_int - 1) - 1)
            den = p_int
            
            g = math.gcd(num, den)
            N = num // g
            M = den // g
            
            congruence_holds = (N % p_int == 0) and (M % p_int != 0)
            neg_q = not congruence_holds
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: a and b are integers",
    "¬Q: q_p(ab) is not congruent to q_p(a) + q_p(b) mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2