import sympy
import math
from sympy.abc import x, y, z

# Top-level setup
# Witnesses are expected to be tuples of 4 integers: (R_mod, S_mod, f_map, M_gen)
# representing the rings Z/R_mod Z and Z/S_mod Z, the map f(x) = f_map * x, and the ideal <M_gen>.
# Alternatively, a dictionary with keys 'R_mod', 'S_mod', 'f_map', 'M_gen' can be provided.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R_mod = int(witness['R_mod'])
            S_mod = int(witness['S_mod'])
            f_map = int(witness['f_map'])
            M_gen = int(witness['M_gen'])
        elif hasattr(witness, 'R_mod'):
            R_mod = int(witness.R_mod)
            S_mod = int(witness.S_mod)
            f_map = int(witness.f_map)
            M_gen = int(witness.M_gen)
        else:
            R_mod, S_mod, f_map, M_gen = map(int, witness)
    except Exception:
        return [False, False, False, False]

    # H1: R and S are commutative rings
    try:
        h1 = (R_mod >= 0) and (S_mod >= 0)
    except Exception:
        h1 = False

    # H2: f: R \to S is a surjective ring homomorphism
    try:
        if S_mod == 0:
            h2 = (R_mod == 0) and (f_map == 1)
        elif S_mod == 1:
            h2 = True
        else:
            h2 = (R_mod % S_mod == 0) and (f_map % S_mod == 1)
    except Exception:
        h2 = False

    # H3: M is a maximal ideal of R
    try:
        M_val = abs(M_gen)
        if R_mod == 0:
            h3 = sympy.isprime(M_val)
        elif R_mod == 1:
            h3 = False
        else:
            h3 = sympy.isprime(M_val) and (R_mod % M_val == 0)
    except Exception:
        h3 = False

    # neg_Q: f(M) is NOT a maximal ideal of S
    try:
        M_val = abs(M_gen)
        if S_mod == 0:
            is_max = sympy.isprime(M_val)
        elif S_mod == 1:
            is_max = False
        else:
            is_max = sympy.isprime(math.gcd(M_val, S_mod))
        neg_q = not is_max
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: f: R \\to S is a surjective ring homomorphism",
    "H_3: M is a maximal ideal of R",
    "¬Q: f(M) is not a maximal ideal of S"
]

N_HYP = 3
NEG_Q_INDEX = 3