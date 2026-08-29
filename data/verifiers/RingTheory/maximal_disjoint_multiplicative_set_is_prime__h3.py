import sympy
from sympy.ntheory import divisors

Z2 = 2
Z3 = 3
Z4 = 4
Z6 = 6

def conditions(witness) -> list[bool]:
    try:
        n, S_list, I_list = witness
        n = int(n)
        S = set(x % n for x in S_list)
        I = set(x % n for x in I_list)
        
        h1 = (n >= 2)
        
        h2 = all((a * b) % n in S for a in S for b in S)
        
        ideals = []
        for d in divisors(n):
            ideals.append(set((k * d) % n for k in range(n)))
            
        if I not in ideals:
            h3 = False
        else:
            h3 = True
            for J in ideals:
                if I.issubset(J) and I != J:
                    if not J.intersection(S):
                        h3 = False
                        break
                        
        R_set = set(range(n))
        if I == R_set:
            is_prime = False
        else:
            is_prime = True
            for a in R_set - I:
                for b in R_set - I:
                    if (a * b) % n in I:
                        is_prime = False
                        break
                if not is_prime:
                    break
                    
        neg_q = not is_prime
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: For any ideal J strictly containing I, J intersection S is non-empty",
    "¬Q: I is not a prime ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3