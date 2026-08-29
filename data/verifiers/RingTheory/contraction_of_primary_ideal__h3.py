import math
from sympy.ntheory import factorint
from sympy import ZZ, QQ

# Top-level setup for potential witness expressions
Z = 0
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z12 = 12

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: The contraction f^{-1}(Q) is not an f^{-1}(P)-primary ideal in R"
]

def get_modulus(ring):
    if isinstance(ring, int):
        return ring
    if ring.__class__.__name__ == 'IntegerRing':
        return 0
    if str(ring) == 'ZZ':
        return 0
    try:
        return int(ring)
    except Exception:
        return None

def get_gen(ideal):
    if isinstance(ideal, int):
        return abs(ideal)
    if hasattr(ideal, 'gen'):
        return abs(ideal.gen)
    if hasattr(ideal, 'args') and len(ideal.args) > 0:
        try:
            return abs(int(ideal.args[0]))
        except Exception:
            pass
    try:
        return abs(int(ideal))
    except Exception:
        return None

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, dict):
            R = witness.get('R', 0)
            S = witness.get('S', 0)
            Q = witness.get('Q', 0)
            P = witness.get('P', 0)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 5:
                R, S, f, Q, P = witness
            elif len(witness) == 4:
                R, S, Q, P = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        n = get_modulus(R)
        m = get_modulus(S)
        q = get_gen(Q)
        p = get_gen(P)

        if any(x is None for x in [n, m, q, p]):
            return [False, False, False]

        # H_1: R and S are commutative rings with identity
        # We represent rings as Z/nZ and Z/mZ, which are always commutative rings with identity
        h1_ok = isinstance(n, int) and isinstance(m, int) and n >= 0 and m >= 0

        # H_2: f: R -> S is a ring homomorphism
        # The canonical map Z/nZ -> Z/mZ is a ring homomorphism iff m divides n (when n > 0)
        # If n == 0 (R=Z), it's always a homomorphism to Z/mZ
        if m == 0:
            h2_ok = (n == 0)
        else:
            h2_ok = (n == 0) or (n % m == 0)

        # ¬Q: The contraction f^{-1}(Q) is not an f^{-1}(P)-primary ideal in R
        # Calculate generators for f^{-1}(Q) and f^{-1}(P) in R
        if m > 0:
            q_z = math.gcd(q, m)
            p_z = math.gcd(p, m)
        else:
            q_z = q
            p_z = p

        if n > 0:
            inv_q = math.gcd(q_z, n)
            inv_p = math.gcd(p_z, n)
        else:
            inv_q = q_z
            inv_p = p_z

        # Check if f^{-1}(Q) is primary in Z/nZ
        if inv_q == 1:
            is_prim = False
            rad = 1
        elif inv_q == 0:
            is_prim = True
            rad = 0
        else:
            factors = factorint(inv_q)
            if len(factors) == 1:
                is_prim = True
            else:
                is_prim = False
            rad = 1
            for prime in factors:
                rad *= prime

        # Check if its radical is f^{-1}(P)
        if n > 0:
            rad_gen = math.gcd(rad, n)
        else:
            rad_gen = rad

        is_inv_p_primary = is_prim and (rad_gen == inv_p)
        neg_q_ok = not is_inv_p_primary

        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]