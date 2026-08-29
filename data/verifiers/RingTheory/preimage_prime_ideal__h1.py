import sympy
from sympy import Rational

# Witness should be a dict: {'n': int, 'm': int, 'k': int, 'P': list[int]}
# representing a ring homomorphism f: Z/nZ -> Z/mZ, f(x) = kx mod m,
# and an ideal P in Z/mZ.
# Alternatively, a tuple (n, m, k, P) is accepted.

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = int(witness['n'])
            m = int(witness['m'])
            k = int(witness['k'])
            P = set(witness['P'])
        else:
            n, m, k, P = witness
            n = int(n)
            m = int(m)
            k = int(k)
            P = set(P)
    except Exception:
        return [False, False, False]

    # H_1: f is a ring homomorphism from R to S
    try:
        if n <= 0 or m <= 0:
            h1 = False
        else:
            # f(x) = kx mod m
            # Preserves addition: k(x+y) = kx + ky mod m (always true)
            # Preserves multiplication: k(xy) = (kx)(ky) mod m => k = k^2 mod m
            # Well-defined: x = y mod n => f(x) = f(y) mod m => kn = 0 mod m
            h1 = ((k * k) % m == k % m) and ((k * n) % m == 0)
    except Exception:
        h1 = False

    # H_2: P is a prime ideal of S
    try:
        if not P.issubset(set(range(m))):
            h2 = False
        else:
            is_ideal = True
            if 0 not in P:
                is_ideal = False
            for x in P:
                for y in P:
                    if (x - y) % m not in P:
                        is_ideal = False
                for r in range(m):
                    if (r * x) % m not in P:
                        is_ideal = False
            
            is_proper = (1 not in P) and (len(P) < m)
            
            is_prime = True
            for a in range(m):
                for b in range(m):
                    if (a * b) % m in P:
                        if a not in P and b not in P:
                            is_prime = False
            
            h2 = is_ideal and is_proper and is_prime
    except Exception:
        h2 = False

    # ¬Q: The preimage f^{-1}(P) is not a prime ideal of R
    try:
        f_inv_P = set()
        for x in range(n):
            if (k * x) % m in P:
                f_inv_P.add(x)
        
        is_ideal = True
        if 0 not in f_inv_P:
            is_ideal = False
        for x in f_inv_P:
            for y in f_inv_P:
                if (x - y) % n not in f_inv_P:
                    is_ideal = False
            for r in range(n):
                if (r * x) % n not in f_inv_P:
                    is_ideal = False
        
        is_proper = (1 not in f_inv_P) and (len(f_inv_P) < n)
        
        is_prime = True
        for a in range(n):
            for b in range(n):
                if (a * b) % n in f_inv_P:
                    if a not in f_inv_P and b not in f_inv_P:
                        is_prime = False
        
        neg_q = not (is_ideal and is_proper and is_prime)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: P is a prime ideal of S",
    "¬Q: The preimage f^{-1}(P) is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2