import sympy
from sympy.ntheory import factorint

# Top-level setup
# Witnesses for finite rings are typically provided as a tuple (n, S),
# where n is an integer >= 2 representing the commutative ring Z/nZ,
# and S is a list or set of integers representing the subset.

def conditions(witness):
    try:
        # Extract ring representation n and subset S
        if isinstance(witness, dict):
            n = witness.get('n', witness.get('R'))
            S = witness.get('S')
        else:
            n, S = witness
            
        if hasattr(n, 'is_Integer') and n.is_Integer:
            n = int(n)
            
        # H_1: R is a commutative ring
        # We check if n is a valid modulus for Z/nZ and S is a valid collection
        h1 = isinstance(n, int) and n >= 2 and isinstance(S, (list, set, tuple))
        if not h1:
            return [False, False, False]
            
        # H_2: 0 is not an element of S
        # In Z/nZ, 0 is represented by elements congruent to 0 modulo n
        h2 = all(int(s) % n != 0 for s in S)
        
        # ¬Q: The intersection of S and the nilradical of R is not empty
        # The nilradical of Z/nZ consists of all multiples of the radical of n
        # (the product of all distinct prime factors of n).
        factors = factorint(n)
        rad_n = 1
        for p in factors:
            rad_n *= p
            
        nilradical = set((k * rad_n) % n for k in range(n))
        S_mod = set(int(s) % n for s in S)
        
        neg_q = len(S_mod.intersection(nilradical)) > 0
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: 0 is not an element of S",
    "¬Q: The intersection of S and the nilradical of R is not empty"
]

N_HYP = 2
NEG_Q_INDEX = 2