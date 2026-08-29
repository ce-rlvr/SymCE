import math

# Top-level setup
# The witness is expected to be a tuple (n, a, b) representing:
# - The ring R = Z/nZ (with n=0 representing Z)
# - The ideal I = <a>
# - The ideal J = <b>
Z = 0

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n', 0)
            a = witness.get('a', 0)
            b = witness.get('b', 0)
        else:
            n, a, b = witness
        n, a, b = abs(int(n)), int(a), int(b)
    except Exception:
        return [False, False, False, False]
        
    # H1: R is a commutative ring with identity
    # Z/nZ is always a commutative ring with identity.
    h1 = True
    
    # H2: I and J are ideals of R
    # <a> and <b> are always ideals in Z/nZ.
    h2 = True
    
    # H3: I + J = R
    # In Z/nZ, I + J = <a, b>. This equals R iff gcd(a, b, n) == 1.
    try:
        if n == 0:
            h3 = (math.gcd(a, b) == 1)
        else:
            h3 = (math.gcd(math.gcd(a, b), n) == 1)
    except Exception:
        h3 = False
        
    # neg_Q: not (exists unique idempotent e such that I = <1-e> and J = <e>)
    try:
        valid_e_count = 0
        if n == 0:
            idempotents = [0, 1]
            for e in idempotents:
                # In Z, <x> == <a> iff abs(x) == abs(a)
                if abs(1 - e) == abs(a) and abs(e) == abs(b):
                    valid_e_count += 1
        else:
            idempotents = [e for e in range(n) if (e * e) % n == e]
            for e in idempotents:
                # In Z/nZ, <x> == <a> iff gcd(x, n) == gcd(a, n)
                if math.gcd((1 - e) % n, n) == math.gcd(a, n) and math.gcd(e, n) == math.gcd(b, n):
                    valid_e_count += 1
        neg_q = (valid_e_count != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I and J are ideals of R",
    "H_3: I + J = R",
    "¬Q: There does not exist a unique idempotent e such that I = <1-e> and J = <e>"
]

N_HYP = 3
NEG_Q_INDEX = 3