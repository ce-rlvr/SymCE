import sympy

# Top-level setup
# The witness is expected to be a tuple (n, S) representing the ring R = ZZ/nZZ
# and a subset S of ZZ/nZZ. 
# Example of a valid counterexample witness: (12, [3, 9])

def conditions(witness):
    try:
        # Validate witness format
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
            
        n, S_elements = witness
        
        # Restrict n to reasonable integers to ensure fast execution
        if not isinstance(n, (int, sympy.Integer)) or n < 2 or n > 10000:
            return [False, False, False]
            
        try:
            S = set(int(s) % n for s in S_elements)
        except Exception:
            return [False, False, False]
            
        # H_1: S is a multiplicatively closed subset of R
        if len(S) == 0:
            h1 = False
        else:
            h1 = True
            for a in S:
                for b in S:
                    if (a * b) % n not in S:
                        h1 = False
                        break
                if not h1:
                    break
                    
        # H_2: 0 is not an element of S
        h2 = (0 not in S)
        
        # ¬Q: S^{-1}R is NOT an integrally closed domain
        # For R = ZZ/nZZ, the localized ring S^{-1}R is isomorphic to R/I
        # where I = {x in R | exists s in S such that s*x = 0}.
        I = set()
        for x in range(n):
            if any((s * x) % n == 0 for s in S):
                I.add(x)
                
        # The size of the quotient ring R/I is n / |I|
        m = n // len(I)
        
        # S^{-1}R is isomorphic to ZZ/mZZ.
        # A finite ring ZZ/mZZ is an integrally closed domain iff it is a field,
        # which is true if and only if m is prime.
        # If m is composite, it has zero divisors. If m = 1, it is the zero ring.
        is_domain = sympy.isprime(m)
        neg_q = not is_domain
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: 0 is not an element of S",
    "¬Q: S^{-1}R is not an integrally closed domain"
]

N_HYP = 2
NEG_Q_INDEX = 2