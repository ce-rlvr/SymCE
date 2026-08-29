import math
from sympy.ntheory import factorint

def get_N(q, a, b):
    """
    Computes the number of projective points on the elliptic curve 
    y^2 = x^3 + ax + b over the ring Z/qZ.
    Assumes gcd(16*(4a^3 + 27b^2), q) == 1, which implies q is odd and 
    the curve is smooth over Z/qZ.
    """
    factors = factorint(q)
    N = 1
    for p, e in factors.items():
        pts = 0
        for x in range(p):
            rhs = (x**3 + a*x + b) % p
            if rhs == 0:
                pts += 1
            else:
                # Euler's criterion for quadratic residues mod p (p is odd)
                leg = pow(rhs, (p - 1) // 2, p)
                if leg == 1:
                    pts += 2
        # Add 1 for the point at infinity
        Np = pts + 1
        # By Hensel's Lemma, the number of points over Z/p^e Z is p^(e-1) * N_p
        N *= (p**(e - 1)) * Np
    return N

def extract(witness):
    """
    Extracts q, a, b, and optionally N from the witness.
    Supports dicts, objects with attributes, and tuples/lists.
    """
    if isinstance(witness, dict):
        q, a, b = witness['q'], witness['a'], witness['b']
        N = witness.get('N', None)
    elif hasattr(witness, 'q'):
        q, a, b = witness.q, witness.a, witness.b
        N = getattr(witness, 'N', None)
    else:
        q, a, b = witness[0], witness[1], witness[2]
        N = witness[3] if len(witness) > 3 else None
    return q, a, b, N

def conditions(witness):
    try:
        q, a, b, N_wit = extract(witness)
        
        # H_1: E is an elliptic curve defined over F_q
        # In the context of this false conjecture, F_q is mistakenly treated as Z/qZ.
        # We verify that q is a valid modulus and the curve is smooth over Z/qZ.
        h1 = (isinstance(q, int) and 2 <= q <= 100000 and 
              isinstance(a, int) and isinstance(b, int) and 
              math.gcd(16 * (4 * a**3 + 27 * b**2), q) == 1)
    except Exception:
        h1 = False

    try:
        if h1:
            true_N = get_N(q, a, b)
            if N_wit is None:
                # If N is not provided, we compute it as defined by the hypothesis
                N = true_N
                h2 = True
            else:
                # If N is provided, it must be the correct number of points
                N = N_wit
                h2 = (N == true_N)
        else:
            h2 = False
            N = 0
    except Exception:
        h2 = False
        N = 0

    try:
        if h1 and h2:
            # ¬Q: The number of points N does NOT satisfy the Hasse-Weil bound
            neg_q_cond = abs(N - (q + 1)) > 2 * math.sqrt(q)
        else:
            neg_q_cond = False
    except Exception:
        neg_q_cond = False

    return [h1, h2, neg_q_cond]

CONDITION_LABELS = [
    "H_1: E is an elliptic curve defined over F_q",
    "H_2: N is the number of F_q-rational points on E, including the point at infinity",
    "¬Q: The number of points N does not satisfy |N - (q + 1)| <= 2*sqrt(q)"
]

N_HYP = 2
NEG_Q_INDEX = 2