import sympy
import math

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    h1 = False
    neg_q = False
    
    n = None
    N_val = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int) and isinstance(witness[1], int):
                n, N_val = witness
        elif isinstance(witness, dict) and 'n' in witness and 'N' in witness:
            n = int(witness['n'])
            N_val = int(witness['N'])
            
        if n is not None and N_val is not None:
            n = abs(n)
            h1 = True
            
            if n == 0:
                intersection_gen = 0
                ideal_N_gen = abs(N_val)
            elif n == 1:
                intersection_gen = 1
                ideal_N_gen = 1
            else:
                factors = sympy.primefactors(n)
                intersection_gen = 1
                for p in factors:
                    intersection_gen *= p
                ideal_N_gen = math.gcd(N_val, n)
                
            if ideal_N_gen != intersection_gen:
                neg_q = True
            return [h1, neg_q]
    except Exception:
        pass

    try:
        h1 = bool(witness.is_commutative_ring() and witness.has_unity())
    except Exception:
        h1 = False
        
    try:
        neg_q = bool(witness.N != witness.intersection_of_prime_ideals())
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with unity",
    "¬Q: N is not equal to the intersection of all prime ideals of R"
]

N_HYP = 1
NEG_Q_INDEX = 1