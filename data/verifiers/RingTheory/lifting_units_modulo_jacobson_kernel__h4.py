import sympy
from sympy.ntheory import primefactors
from math import gcd

# Top-level setup for witness expressions
# We represent the finite ring Z/nZ simply by the integer n.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    # We expect the witness to represent (R, S, x) or (R, S, f, x)
    # where R and S are given as integers n and m (representing Z/nZ and Z/mZ).
    if isinstance(witness, dict):
        try:
            if 'n' in witness: n = int(witness['n'])
            elif 'R' in witness: n = int(witness['R'])
            else: return [False, False, False, False]
            
            if 'm' in witness: m = int(witness['m'])
            elif 'S' in witness: m = int(witness['S'])
            else: return [False, False, False, False]
            
            if 'x' in witness: x = int(witness['x'])
            else: return [False, False, False, False]
        except Exception:
            return [False, False, False, False]
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            n_val, m_val, x_val = witness
        elif len(witness) == 4:
            n_val, m_val, _, x_val = witness
        else:
            return [False, False, False, False]
        try:
            n = int(n_val)
            m = int(m_val)
            x = int(x_val)
        except Exception:
            return [False, False, False, False]
    else:
        return [False, False, False, False]

    # H_1: R and S are rings
    try:
        h1_ok = bool(n >= 2 and m >= 2)
    except Exception:
        h1_ok = False

    # H_2: f: R -> S is a surjective ring homomorphism
    # The natural projection Z/nZ -> Z/mZ is a surjective ring homomorphism iff m divides n.
    try:
        h2_ok = bool(n % m == 0)
    except Exception:
        h2_ok = False

    # H_3: The kernel of f is contained in the Jacobson radical of R
    # The kernel is mZ/nZ. The Jacobson radical of Z/nZ is rad(n)Z/nZ,
    # where rad(n) is the product of distinct prime factors of n.
    # mZ/nZ is contained in rad(n)Z/nZ iff rad(n) divides m.
    try:
        rad_n = 1
        for p in primefactors(n):
            rad_n *= p
        h3_ok = bool(m % rad_n == 0)
    except Exception:
        h3_ok = False

    # neg_Q: The element x is not a unit in R
    # x is a unit in Z/nZ iff gcd(x, n) == 1.
    try:
        neg_q_ok = bool(gcd(x, n) > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a surjective ring homomorphism",
    "H_3: The kernel of f is contained in the Jacobson radical of R",
    "¬Q: The element x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3