import math
import sympy
from sympy.ntheory import primefactors

# Top-level setup: named object bindings that the witness expression may reference.
# We provide several finite rings Z/nZ (represented by the integer n) 
# which are sufficient to construct a counterexample.
Z6 = 6
Z10 = 10
Z12 = 12
Z14 = 14
Z15 = 15
Z30 = 30

def get_divisors(num):
    divs = set()
    for i in range(1, int(math.isqrt(num)) + 1):
        if num % i == 0:
            divs.add(i)
            divs.add(num // i)
    return divs

def has_valid_s(i, y, n, p):
    """
    Checks if there exists s such that i*s = y (mod n) and s is not divisible by p.
    """
    g = math.gcd(i, n)
    if y % g != 0:
        return False
    if (n // g) % p != 0:
        return True
    
    a = i // g
    b = y // g
    m = n // g
    try:
        inv_a = sympy.mod_inverse(a, m)
    except Exception:
        return False
    s0 = (b * inv_a) % m
    return s0 % p != 0

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, I, J = witness
        
        # Extract the modulo n for the ring Z/nZ
        if hasattr(R, 'mod'):
            try:
                n = int(R.mod)
            except Exception:
                n = None
        else:
            try:
                n = int(R)
            except Exception:
                n = None
                
        if n is None or n < 2:
            return [False, False, False]
            
        # H_1: R is a commutative ring
        # Z/nZ is always a commutative ring for n >= 2
        h1 = True
        
        try:
            I_set = set(int(x) % n for x in I)
            J_set = set(int(x) % n for x in J)
        except Exception:
            return [h1, False, False]
            
        # H_2: I is an ideal of R
        if not I_set:
            h2 = False
        else:
            h2 = True
            # Check closure under addition
            for a in I_set:
                for b in I_set:
                    if (a + b) % n not in I_set:
                        h2 = False
                        break
                if not h2: break
                # Check closure under multiplication by any element in R
                for r in range(n):
                    if (a * r) % n not in I_set:
                        h2 = False
                        break
                if not h2: break
                
        # neg_Q: The equivalence (I \subseteq J iff I_M \subseteq J_M for all M) fails
        I_subset_J = I_set.issubset(J_set)
        
        primes = primefactors(n)
        divs_n = get_divisors(n)
        
        IM_subset_JM_all = True
        for p in primes:
            # Ann_Sc is the set of elements annihilated by some u not in M
            Ann_Sc = set()
            for d in divs_n:
                if d % p != 0:
                    step = n // d
                    for x in range(0, n, step):
                        Ann_Sc.add(x)
                        
            M_condition = True
            for i in I_set:
                found = False
                for j in J_set:
                    for a in Ann_Sc:
                        y = (j + a) % n
                        if has_valid_s(i, y, n, p):
                            found = True
                            break
                    if found:
                        break
                if not found:
                    M_condition = False
                    break
            if not M_condition:
                IM_subset_JM_all = False
                break
                
        neg_q = (I_subset_J != IM_subset_JM_all)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The equivalence (I \\subseteq J iff I_M \\subseteq J_M for all maximal ideals M) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2