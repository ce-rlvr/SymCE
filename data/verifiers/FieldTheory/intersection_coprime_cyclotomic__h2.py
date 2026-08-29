import math
import sympy
from sympy.ntheory import totient

# Top-level setup
# (No specific named objects required for this number theory / field theory witness)

CONDITION_LABELS = [
    "H_1: n and m are positive integers",
    "H_2: ζ_n is a primitive n-th root of unity",
    "H_3: ζ_m is a primitive m-th root of unity",
    "¬Q: The intersection of the fields ℚ(ζ_n) ∩ ℚ(ζ_m) is not ℚ"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # Extract n and m from the witness
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            m = witness.get('m')
        elif hasattr(witness, 'n') and hasattr(witness, 'm'):
            n = witness.n
            m = witness.m
        else:
            n, m = witness[:2]
    except Exception:
        n, m = None, None

    def is_pos_int(x):
        try:
            return (isinstance(x, int) or isinstance(x, sympy.Integer)) and x > 0
        except Exception:
            return False

    # H_1: n and m are positive integers
    try:
        h1 = is_pos_int(n) and is_pos_int(m)
    except Exception:
        h1 = False

    # H_2: ζ_n is a primitive n-th root of unity
    # This mathematically holds as long as n is a positive integer.
    try:
        h2 = is_pos_int(n)
    except Exception:
        h2 = False

    # H_3: ζ_m is a primitive m-th root of unity
    # This mathematically holds as long as m is a positive integer.
    try:
        h3 = is_pos_int(m)
    except Exception:
        h3 = False

    # ¬Q: The intersection of the fields ℚ(ζ_n) ∩ ℚ(ζ_m) is not ℚ
    # By Galois theory, [ℚ(ζ_n) ∩ ℚ(ζ_m) : ℚ] = φ(n) * φ(m) / φ(lcm(n, m))
    # The intersection is strictly larger than ℚ iff this degree is > 1.
    try:
        if h1:
            n_int = int(n)
            m_int = int(m)
            lcm_nm = (n_int * m_int) // math.gcd(n_int, m_int)
            deg_intersection = totient(n_int) * totient(m_int) // totient(lcm_nm)
            neg_q = deg_intersection > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]