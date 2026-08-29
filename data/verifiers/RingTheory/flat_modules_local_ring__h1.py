import math
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

# Standard linear algebra objects that might be used in witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Witness should be a tuple (n, gs) where:
# - n is an integer >= 2, defining the commutative ring R = Z/nZ.
# - gs is a list of integers, defining the R-module M = \bigoplus_{g \in gs} Z/gcd(g,n)Z.
# Example witness for a flat but not free module: (6, [2])

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the conjecture:
    "If M is a finitely generated flat R-module, then M is a free R-module."
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        
        try:
            n = int(witness[0])
        except Exception:
            return [False, False, False]
            
        if n < 2:
            return [False, False, False]
            
        gs_raw = witness[1]
        if not isinstance(gs_raw, (list, tuple)):
            return [False, False, False]
            
        try:
            gs = [int(g) for g in gs_raw]
        except Exception:
            return [False, False, False]
                
        # H1: M is a finitely generated module over R
        # By definition of our witness format, M is a finite direct sum of cyclic modules,
        # so it is always finitely generated.
        h1 = True
        
        # H2: M is a flat R-module
        # Over Z/nZ, M = sum Z/g_i Z is flat iff gcd(g_i, n/g_i) == 1 for all i.
        g_list = [math.gcd(g, n) for g in gs]
        h2 = True
        for g in g_list:
            if math.gcd(g, n // g) != 1:
                h2 = False
                break
                
        # Q: M is a free R-module
        # M is free over Z/nZ iff its invariant factors are all 1 or n.
        # First, find prime factors of n.
        temp = n
        primes = []
        p = 2
        while p * p <= temp:
            if temp % p == 0:
                primes.append(p)
                while temp % p == 0:
                    temp //= p
            p += 1
        if temp > 1:
            primes.append(temp)
            
        # Compute the p-parts of each cyclic summand to find invariant factors
        m = len(g_list)
        p_parts = {}
        for p in primes:
            parts = []
            for g in g_list:
                part = 1
                temp_g = g
                while temp_g % p == 0 and temp_g > 0:
                    part *= p
                    temp_g //= p
                parts.append(part)
            parts.sort()
            p_parts[p] = parts
            
        inv_factors = []
        for i in range(m):
            d = 1
            for p in primes:
                d *= p_parts[p][i]
            inv_factors.append(d)
            
        q = True
        for d in inv_factors:
            if d != 1 and d != n:
                q = False
                break
                
        neg_q = not q
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: M is a finitely generated module over R",
    "H_2: M is a flat R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2