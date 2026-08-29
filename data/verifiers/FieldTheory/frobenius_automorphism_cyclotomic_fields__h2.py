import math
from sympy import isprime

# Top-level setup
# No specific named objects required for this domain (witnesses are integers/tuples).

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n_val = witness.get('n')
            p_val = witness.get('p')
            a_val = witness.get('sigma_p', witness.get('a'))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                n_val, p_val = witness
                a_val = None
            elif len(witness) == 3:
                n_val, p_val, a_val = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if n_val is None or p_val is None:
            return [False, False, False, False]
            
        if not isinstance(n_val, (int, float)) or not isinstance(p_val, (int, float)):
            return [False, False, False, False]
            
        if int(n_val) != n_val or int(p_val) != p_val:
            return [False, False, False, False]
            
        n = int(n_val)
        p = int(p_val)
        
        if a_val is not None:
            if not isinstance(a_val, (int, float)) or int(a_val) != a_val:
                return [False, False, False, False]
            a = int(a_val)
        else:
            a = None
            
        # H_1: n is a positive integer
        h1 = (n >= 1)
        
        # H_2: zeta_n is a primitive n-th root of unity in C
        # This is a definitional hypothesis setting the context.
        h2 = h1
        
        if not h1:
            return [False, False, False, False]
            
        # H_3: sigma_p is the Frobenius automorphism at p in Gal(Q(zeta_n)/Q)
        if not isprime(p):
            h3 = False
            neg_q = False
        else:
            # Find the unramified part of n with respect to p
            m = n
            if p > 1:
                while m % p == 0:
                    m //= p
                    
            # If the specific automorphism 'a' is not provided, find a valid one
            if a is None:
                for i in range(1, n + 1):
                    if math.gcd(i, n) == 1 and i % m == p % m:
                        a = i
                        break
                        
            if a is None:
                h3 = False
                neg_q = False
            else:
                # sigma_a is an automorphism iff gcd(a, n) == 1
                # sigma_a is a Frobenius automorphism at p iff a == p (mod m)
                h3 = (math.gcd(a, n) == 1) and (a % m == p % m)
                
                # neg_Q: sigma_p(zeta_n) != zeta_n^p
                # This means zeta_n^a != zeta_n^p, which is equivalent to a != p (mod n)
                neg_q = (a % n != p % n)
                
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: zeta_n is a primitive n-th root of unity in C",
    "H_3: sigma_p is the Frobenius automorphism at p in Gal(Q(zeta_n)/Q)",
    "¬Q: sigma_p(zeta_n) != zeta_n^p"
]

N_HYP = 3
NEG_Q_INDEX = 3