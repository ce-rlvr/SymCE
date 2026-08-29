import sympy
from sympy.abc import x, y, z

def conditions(witness):
    """
    Expects witness to be a tuple: (n, S_list, s)
    where:
      n: int >= 0, representing the ring Z/nZ (n=0 means Z)
      S_list: list of ints, representing the subset S
      s: int, representing the element s
    """
    try:
        n, S_list, s = witness
        if str(n) == 'ZZ':
            n = 0
        else:
            n = int(n)
        S_list = [int(e) for e in S_list]
        s = int(s)
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring with identity
    try:
        h1 = (n >= 0)
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    try:
        if n > 0:
            S_set = set(e % n for e in S_list)
            s_norm = s % n
        else:
            S_set = set(S_list)
            s_norm = s
            
        if not S_set:
            h2 = False
        else:
            h2 = True
            for a in S_set:
                for b in S_set:
                    prod = (a * b) % n if n > 0 else (a * b)
                    if prod not in S_set:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: s is an element of S
    try:
        h3 = s_norm in S_set
    except Exception:
        h3 = False

    # neg_Q: The fraction s/1 is NOT a unit in S^(-1)R
    # If 1 is in S, s/1 is always a valid fraction and a unit (its inverse is 1/s).
    # If 1 is not in S, s/1 is not a valid fraction in S^(-1)R, hence it cannot be a unit.
    try:
        identity = 1 % n if n > 0 else 1
        neg_q = identity not in S_set
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: s is an element of S",
    "¬Q: The fraction s/1 is not a unit in S^(-1)R"
]

N_HYP = 3
NEG_Q_INDEX = 3