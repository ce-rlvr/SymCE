import math

# Top-level setup
Z = 'Z'
Z2 = ('Z', 2)
Z3 = ('Z', 3)
Z4 = ('Z', 4)
Z5 = ('Z', 5)
Z6 = ('Z', 6)
Z8 = ('Z', 8)
Z12 = ('Z', 12)

def is_commutative_ring(ring):
    if ring == 'Z':
        return True
    if isinstance(ring, tuple) and len(ring) == 2 and ring[0] == 'Z' and isinstance(ring[1], int) and ring[1] > 0:
        return True
    return False

def get_generator(ring, ideal):
    if isinstance(ideal, int):
        gens = [ideal]
    elif isinstance(ideal, (list, tuple, set)):
        gens = list(ideal)
    else:
        gens = [int(ideal)]
    
    if ring == 'Z':
        g = 0
        for x in gens:
            g = math.gcd(g, int(x))
        return abs(g)
    elif isinstance(ring, tuple) and ring[0] == 'Z':
        n = ring[1]
        g = n
        for x in gens:
            g = math.gcd(g, int(x))
        return abs(g) % n
    else:
        raise ValueError("Unknown ring")

def is_ideal(ring, ideal):
    try:
        get_generator(ring, ideal)
        return True
    except Exception:
        return False

def ideal_mul(ring, I, J):
    gI = get_generator(ring, I)
    gJ = get_generator(ring, J)
    return get_generator(ring, gI * gJ)

def ideal_eq(ring, I, J):
    return get_generator(ring, I) == get_generator(ring, J)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            ring = witness.get('R', witness.get('ring', 'Z'))
            I = witness['I']
            J = witness['J']
            K = witness['K']
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            ring, I, J, K = witness
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            ring = 'Z'
            I, J, K = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = is_commutative_ring(ring)
    except Exception:
        h1 = False

    # H_2: I, J, and K are ideals of R
    try:
        h2 = is_ideal(ring, I) and is_ideal(ring, J) and is_ideal(ring, K)
    except Exception:
        h2 = False

    # H_3: IJ = IK
    try:
        h3 = ideal_eq(ring, ideal_mul(ring, I, J), ideal_mul(ring, I, K))
    except Exception:
        h3 = False

    # ¬Q: J != K
    try:
        neg_q = not ideal_eq(ring, J, K)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I, J, and K are ideals of R",
    "H_3: IJ = IK",
    "¬Q: J != K"
]

N_HYP = 3
NEG_Q_INDEX = 3