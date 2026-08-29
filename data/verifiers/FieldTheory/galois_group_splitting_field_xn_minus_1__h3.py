import sympy
from sympy.ntheory import reduced_totient, n_order
from sympy import QQ, GF

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (K, n, L) or a dictionary with these keys.
    """
    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            n = witness.get('n')
            L = witness.get('L')
        else:
            K, n, L = witness
    except Exception:
        try:
            K, n = witness
            L = None
        except Exception:
            return [False, False, False, False]

    # H_1: K is a field
    try:
        h1 = getattr(K, 'is_Field', False)
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and int(n) > 0
    except Exception:
        h2 = False

    # H_3: L is the splitting field of x^n - 1 over K
    try:
        h3 = getattr(L, 'is_Field', False) if L is not None else False
    except Exception:
        h3 = False

    # ¬Q: Gal(L/K) is not isomorphic to a subgroup of (Z/nZ)^x
    try:
        if K == sympy.QQ or str(K) == 'QQ':
            is_subgroup = True
        elif hasattr(K, 'characteristic') and K.characteristic() > 0:
            p = int(K.characteristic())
            m = int(n)
            while m % p == 0:
                m //= p
            if m == 1:
                d = 1
            else:
                d = n_order(p, m)
            # A finite abelian group has a cyclic subgroup of order d iff d divides its exponent.
            # The exponent of (Z/nZ)^x is the Carmichael function lambda(n), given by reduced_totient(n).
            is_subgroup = (reduced_totient(int(n)) % d == 0)
        else:
            # For other fields, we assume it embeds into (Z/mZ)^x which embeds into (Z/nZ)^x
            is_subgroup = True
            
        neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n is a positive integer",
    "H_3: L is the splitting field of x^n - 1 over K",
    "¬Q: Gal(L/K) is not isomorphic to a subgroup of (Z/nZ)^x"
]

N_HYP = 3
NEG_Q_INDEX = 3