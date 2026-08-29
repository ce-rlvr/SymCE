import sympy

def get_n(witness):
    try:
        if isinstance(witness, int):
            return witness
        if hasattr(witness, 'is_Integer') and witness.is_Integer:
            return int(witness)
        if isinstance(witness, str):
            s = witness.strip().replace(' ', '')
            if s.startswith("Z/") and s.endswith("Z"):
                return int(s[2:-1])
    except Exception:
        pass
    return -1

def conditions(witness):
    try:
        if witness == sympy.QQ or witness == sympy.ZZ:
            return [True, False]
    except Exception:
        pass

    n = get_n(witness)
    
    try:
        # We interpret an integer n > 0 as the ring Z/nZ, and n == 0 as Z.
        # Both Z and Z/nZ are commutative Noetherian rings.
        h1 = (n >= 0)
    except Exception:
        h1 = False

    try:
        if n > 0:
            # For Z/nZ (n >= 1):
            # A Unique Factorization Domain must be an integral domain.
            # Z/nZ is an integral domain if and only if n is prime.
            is_ufd = sympy.isprime(n)
            
            # The Krull dimension of Z/nZ is 0 (all prime ideals are maximal).
            # Therefore, there are no prime ideals of height 1.
            # The statement "every prime ideal of height 1 is principal" is vacuously TRUE.
            height_1_principal = True
            
            q = (is_ufd == height_1_principal)
            neg_q = not q
        elif n == 0:
            # For Z:
            # Z is a UFD, and every height 1 prime ideal (p) is principal.
            is_ufd = True
            height_1_principal = True
            q = (is_ufd == height_1_principal)
            neg_q = not q
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: The biconditional 'R is a UFD iff every prime ideal of height 1 is principal' fails"
]

N_HYP = 1
NEG_Q_INDEX = 1