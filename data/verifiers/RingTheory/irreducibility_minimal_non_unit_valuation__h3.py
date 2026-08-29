import sympy
from sympy import ZZ

# Top-level setup
# ZZ is provided so the witness can reference it directly.
# The witness is expected to be a tuple (R, d, x) or a dict with keys 'R', 'd', 'x'.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, d, x = witness
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            R = witness.get('R')
            d = witness.get('d')
            x = witness.get('x')
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: R is a Euclidean domain
    try:
        # We verify against the integers as the standard Euclidean domain
        h1 = (R == ZZ or R == sympy.S.Integers)
    except Exception:
        h1 = False

    d_cache = {}
    def get_d(n):
        if n not in d_cache:
            val = d(sympy.Integer(n))
            if val < 0 or int(val) != val:
                raise ValueError("d must return a non-negative integer")
            d_cache[n] = int(val)
        return d_cache[n]

    # H2: d is a submultiplicative Euclidean function on R
    try:
        h2 = False
        if h1:
            is_euclidean = True
            # Check the division algorithm property empirically over a range
            for a_val in range(-20, 21):
                for b_val in range(-20, 21):
                    if b_val == 0: continue
                    db = get_d(b_val)
                    found = False
                    for q_val in range(-40, 41):
                        r = a_val - q_val * b_val
                        if r == 0 or get_d(r) < db:
                            found = True
                            break
                    if not found:
                        is_euclidean = False
                        break
                if not is_euclidean:
                    break
            
            is_submult = True
            if is_euclidean:
                # Check submultiplicativity: d(ab) <= d(a)d(b)
                for a_val in range(-20, 21):
                    if a_val == 0: continue
                    da = get_d(a_val)
                    for b_val in range(-20, 21):
                        if b_val == 0: continue
                        db = get_d(b_val)
                        if get_d(a_val * b_val) > da * db:
                            is_submult = False
                            break
                    if not is_submult:
                        break
            h2 = is_euclidean and is_submult
    except Exception:
        h2 = False

    # H3: d(x) is minimal among all non-zero non-units in R
    try:
        h3 = False
        if h1:
            min_non_unit_d = float('inf')
            # In ZZ, units are 1 and -1. 0 is excluded.
            for i_val in range(-50, 51):
                if i_val in (0, 1, -1): continue
                val = get_d(i_val)
                if val < min_non_unit_d:
                    min_non_unit_d = val
            
            h3 = (get_d(int(x)) == min_non_unit_d)
    except Exception:
        h3 = False

    # neg_Q: x is NOT an irreducible element in R
    try:
        neg_q = False
        if h1:
            # In ZZ, irreducible elements are primes and negative primes.
            # Units (1, -1) and 0 are NOT irreducible.
            neg_q = not sympy.isprime(abs(int(x)))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: d is a submultiplicative Euclidean function on R",
    "H_3: d(x) is minimal among all non-zero non-units in R",
    "¬Q: x is not an irreducible element in R"
]

N_HYP = 3
NEG_Q_INDEX = 3