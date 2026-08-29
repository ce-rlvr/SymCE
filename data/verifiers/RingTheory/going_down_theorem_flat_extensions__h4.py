import sympy
from sympy import S

# Top-level setup: named object bindings that the witness expression may reference.
Z = S.Integers
Q = S.Rationals
R_field = S.Reals
C_field = S.Complexes

def parse_ring(ring):
    if isinstance(ring, str):
        return ring
    if ring == S.Integers: return 'Z'
    if ring == S.Rationals: return 'Q'
    if ring == S.Reals: return 'R'
    if ring == S.Complexes: return 'C'
    return str(ring)

def parse_ideal(I):
    try:
        val = int(I)
        return abs(val)
    except Exception:
        return I

def is_commutative_ring(ring):
    return ring in ['Z', 'Q', 'R', 'C', 'Z[x]', 'Q[x]']

def is_subring(R, S_ring):
    subrings = {
        'Z': ['Z'],
        'Q': ['Z', 'Q'],
        'R': ['Z', 'Q', 'R'],
        'C': ['Z', 'Q', 'R', 'C'],
        'Z[x]': ['Z', 'Z[x]'],
        'Q[x]': ['Z', 'Q', 'Z[x]', 'Q[x]']
    }
    return R in subrings.get(S_ring, [])

def is_flat(R, S_ring):
    if R == S_ring: return True
    if R == 'Z' and S_ring in ['Q', 'R', 'C', 'Z[x]', 'Q[x]']: return True
    if R == 'Q' and S_ring in ['R', 'C', 'Q[x]']: return True
    if R == 'R' and S_ring in ['C', 'R[x]']: return True
    return False

def is_prime_ideal(I, ring):
    if ring == 'Z':
        if I == 0: return True
        if isinstance(I, int) and sympy.isprime(abs(I)): return True
        return False
    if ring in ['Q', 'R', 'C']:
        return I == 0
    return False

def ideal_intersection(I, S_ring, R):
    if S_ring in ['Q', 'R', 'C'] and R == 'Z':
        if I == 0: return 0
    if S_ring == R:
        return I
    if S_ring in ['R', 'C'] and R == 'Q':
        if I == 0: return 0
    return None

def ideal_subset(I1, I2, ring):
    if ring in ['Q', 'R', 'C']:
        return I1 == 0 and I2 == 0
    if ring == 'Z':
        if I2 == 0: return I1 == 0
        if I1 == 0: return True
        return I1 % I2 == 0
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = parse_ring(witness.get('R'))
            S_ring = parse_ring(witness.get('S'))
            P1 = parse_ideal(witness.get('P1'))
            P2 = parse_ideal(witness.get('P2'))
            Q2 = parse_ideal(witness.get('Q2'))
        else:
            R, S_ring, P1, P2, Q2 = witness
            R = parse_ring(R)
            S_ring = parse_ring(S_ring)
            P1 = parse_ideal(P1)
            P2 = parse_ideal(P2)
            Q2 = parse_ideal(Q2)
    except Exception:
        return [False] * 4 + [False]

    # H1: R and S are commutative rings
    try:
        h1 = is_commutative_ring(R) and is_commutative_ring(S_ring)
    except Exception:
        h1 = False

    # H2: R is a subring of S
    try:
        h2 = is_subring(R, S_ring)
    except Exception:
        h2 = False

    # H3: S is a flat R-module
    try:
        h3 = is_flat(R, S_ring)
    except Exception:
        h3 = False

    # H4: Q_2 is a prime ideal of S such that Q_2 \cap R = P_2
    try:
        h4 = is_prime_ideal(Q2, S_ring) and ideal_intersection(Q2, S_ring, R) == P2
    except Exception:
        h4 = False

    # Conclusion: There exists a prime ideal Q_1 of S such that Q_1 \subseteq Q_2 and Q_1 \cap R = P_1
    try:
        if S_ring in ['Q', 'R', 'C']:
            prime_ideals_S = [0]
        elif S_ring == 'Z':
            prime_ideals_S = None
        else:
            prime_ideals_S = []

        conclusion_holds = False
        if prime_ideals_S is not None:
            for Q1 in prime_ideals_S:
                if ideal_subset(Q1, Q2, S_ring) and ideal_intersection(Q1, S_ring, R) == P1:
                    conclusion_holds = True
                    break
        else:
            if S_ring == 'Z' and R == 'Z':
                Q1 = P1
                if is_prime_ideal(Q1, S_ring) and ideal_subset(Q1, Q2, S_ring):
                    conclusion_holds = True

        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: R is a subring of S",
    "H_3: S is a flat R-module",
    r"H_4: Q_2 is a prime ideal of S such that Q_2 \cap R = P_2",
    r"¬Q: There does not exist a prime ideal Q_1 of S such that Q_1 \subseteq Q_2 and Q_1 \cap R = P_1"
]

N_HYP = 4
NEG_Q_INDEX = 4