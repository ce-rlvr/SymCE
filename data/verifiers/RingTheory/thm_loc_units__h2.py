import math
from sympy.ntheory import factorint

# Top-level setup
# Witnesses should be provided as a dictionary, tuple, or object containing:
# - n: modulus of the ring Z/nZ (use 0 for Z)
# - S: list of elements in the subset S
# - a: element a in R
# - s: element s in S
# Example counterexample: witness = (12, [2], 4, 2)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness['n']
            S = witness['S']
            a = witness['a']
            s = witness['s']
        elif isinstance(witness, (tuple, list)):
            n, S, a, s = witness
        else:
            n = witness.n
            S = witness.S
            a = witness.a
            s = witness.s
            
        n = abs(int(n))
        S = [int(x) for x in S]
        a = int(a)
        s = int(s)
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring
    # We represent R as Z/nZ or Z, which are always commutative rings.
    h1 = True
    
    # H2: a is an element of R
    # a is an integer, so it represents an element of R.
    h2 = True
    
    # H3: s is an element of S
    try:
        if n > 0:
            S_mod = [x % n for x in S]
            h3 = (s % n) in S_mod
        else:
            h3 = s in S
    except Exception:
        h3 = False
        
    # neg_Q: a/s is a unit in S^{-1}R iff exists b in R such that ab in S is FALSE
    try:
        if n > 0:
            # Compute M, the multiplicative closure of S modulo n
            M = set([1 % n])
            queue = [1 % n]
            S_mod = [x % n for x in S]
            while queue:
                curr = queue.pop(0)
                for x in S_mod:
                    nxt = (curr * x) % n
                    if nxt not in M:
                        M.add(nxt)
                        queue.append(nxt)
            
            # a/s is a unit in S^{-1}R iff a divides some element in M
            g = math.gcd(a % n, n)
            is_unit = any(m % g == 0 for m in M)
            
            # exists b in R such that ab in S
            exists_b = False
            for x in S_mod:
                if x % g == 0:
                    exists_b = True
                    break
        else:
            # For Z (n=0), M is the set of all finite products of elements in S
            if 0 in S:
                is_unit = True
            elif a == 0:
                is_unit = False
            elif a in [1, -1]:
                is_unit = True
            else:
                # a divides some element in M iff every prime factor of a divides some element in S
                factors = factorint(abs(a))
                is_unit = True
                for p in factors:
                    if not any(x % p == 0 for x in S):
                        is_unit = False
                        break
            
            # exists b in R such that ab in S
            exists_b = False
            if a == 0:
                exists_b = (0 in S)
            else:
                for x in S:
                    if x % a == 0:
                        exists_b = True
                        break
                        
        neg_q = not (is_unit == exists_b)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: a is an element of R",
    "H_3: s is an element of S",
    "¬Q: The fraction a/s is a unit in S^{-1}R if and only if there exists an element b in R such that the product ab is in S is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3