import sympy
from sympy import symbols

# Top-level setup
# Expected witness format:
# A dictionary representing finite rings Z_n and functions as value lists.
# witness = {
#     'R': 2,                 # Modulus for domain ring Z_2
#     'S': [2, 3],            # Moduli for codomain rings Z_2, Z_3
#     'f': [[0, 1], [0, 1]]   # f_i(x) values. f[i][x] is the value of f_i(x)
# }

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            f = witness.get('f')
        else:
            R, S, f = witness

        # H1: R is a ring (represented by modulus n >= 1)
        h1 = isinstance(R, int) and R >= 1

        # H2: {S_i} is a family of rings (represented by list of moduli)
        h2 = isinstance(S, list) and all(isinstance(m, int) and m >= 1 for m in S)

        # H3: f is defined by f(x) = (f_i(x))
        # We verify f is a list of value lists for each f_i
        h3 = isinstance(f, list) and len(f) == len(S)
        if h3:
            for i, m in enumerate(S):
                if not (isinstance(f[i], list) and len(f[i]) == R):
                    h3 = False
                    break
                if not all(isinstance(y, int) and 0 <= y < m for y in f[i]):
                    h3 = False
                    break

        # neg_Q: The conclusion FAILS.
        # The conclusion asserts that f has a kernel (which implies f is a ring homomorphism)
        # and that it equals the intersection of ker(f_i).
        # Since f(x)=0 iff all f_i(x)=0, the set equality always holds.
        # The only way the conclusion fails is if f is NOT a ring homomorphism,
        # meaning "the kernel of f" is undefined in the category of rings.
        
        def is_ring_hom(domain, codomain, func):
            for x in range(domain):
                for y in range(domain):
                    if func[(x + y) % domain] != (func[x] + func[y]) % codomain:
                        return False
                    if func[(x * y) % domain] != (func[x] * func[y]) % codomain:
                        return False
            if func[1 % domain] != 1 % codomain:
                return False
            return True

        is_hom = True
        if h1 and h2 and h3:
            for i, m in enumerate(S):
                if not is_ring_hom(R, m, f[i]):
                    is_hom = False
                    break
        else:
            is_hom = False

        neg_q = not is_hom

        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: {S_i} is a family of rings",
    "H_3: f is defined by f(x) = (f_i(x))",
    "¬Q: f is not a ring homomorphism, so its kernel is undefined"
]

N_HYP = 3
NEG_Q_INDEX = 3