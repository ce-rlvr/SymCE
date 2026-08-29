import sympy
from sympy import Rational, Integer

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Expects witness to be a dictionary or object with:
      - n: int (defines R = Z/nZ)
      - m: int (defines S = Z/mZ, where m=0 means S=Z)
      - f: list of ints of length n, or a callable (defines the map R -> S)
    """
    h1_ok = False
    h2_ok = False
    neg_q_ok = False

    try:
        if isinstance(witness, dict):
            n = int(witness.get('n', -1))
            m = int(witness.get('m', -1))
            f_input = witness.get('f', [])
        else:
            n = int(getattr(witness, 'n', -1))
            m = int(getattr(witness, 'm', -1))
            f_input = getattr(witness, 'f', [])
            
        if callable(f_input):
            f = [int(f_input(i)) for i in range(n)]
        else:
            f = [int(i) for i in f_input]
    except Exception:
        return [False, False, False]

    # H1: R is a local ring with unique maximal ideal M
    p = None
    try:
        if n > 1:
            factors = sympy.factorint(n)
            if len(factors) == 1:
                h1_ok = True
                p = list(factors.keys())[0]
    except Exception:
        pass

    # H2: S is a non-zero ring
    try:
        if m == 0 or m > 1:
            h2_ok = True
    except Exception:
        pass

    # neg_Q: f is a ring homomorphism and its kernel is not a subset of M
    try:
        if h1_ok and h2_ok and len(f) == n:
            def eq_m(a, b, mod):
                if mod == 0:
                    return a == b
                return (a - b) % mod == 0

            is_hom = True
            for i in range(n):
                for j in range(n):
                    if not eq_m(f[(i + j) % n], f[i] + f[j], m):
                        is_hom = False
                        break
                    if not eq_m(f[(i * j) % n], f[i] * f[j], m):
                        is_hom = False
                        break
                if not is_hom:
                    break
            
            if is_hom:
                M = {i for i in range(n) if i % p == 0}
                ker_f = {i for i in range(n) if eq_m(f[i], 0, m)}
                if not ker_f.issubset(M):
                    neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a local ring with unique maximal ideal M",
    "H_2: S is a non-zero ring",
    "¬Q: f is a ring homomorphism and its kernel is not a subset of M"
]

N_HYP = 2
NEG_Q_INDEX = 2