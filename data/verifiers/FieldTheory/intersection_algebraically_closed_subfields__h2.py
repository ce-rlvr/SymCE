import sympy
from sympy import QQ, RR, CC, ZZ

# Top-level setup
# We provide standard domains for the witness to use.
# The witness can be a tuple (E, K_list) where E is a domain and K_list is a list of domains.

def is_field(F):
    if F in (QQ, RR, CC):
        return True
    if hasattr(F, 'is_Field') and F.is_Field:
        return True
    return False

def is_alg_closed(F):
    if F == CC:
        return True
    if hasattr(F, 'is_algebraically_closed'):
        return bool(F.is_algebraically_closed)
    if hasattr(F, 'is_alg_closed'):
        return bool(F.is_alg_closed)
    if F in (QQ, RR, ZZ):
        return False
    return False

def is_subfield(K, E):
    if K == E:
        return True
    if E == CC and K in (QQ, RR):
        return True
    if E == RR and K == QQ:
        return True
    if hasattr(K, 'issubset'):
        try:
            if K.issubset(E): 
                return True
        except Exception:
            pass
    if hasattr(K, 'is_subfield'):
        try:
            if K.is_subfield(E): 
                return True
        except Exception:
            pass
    return False

def intersect_fields(K_list, E):
    if not K_list:
        return E
    res = K_list[0]
    for K in K_list[1:]:
        if res == K:
            continue
        if (res == CC and K == RR) or (res == RR and K == CC):
            res = RR
        elif (res == CC and K == QQ) or (res == QQ and K == CC):
            res = QQ
        elif (res == RR and K == QQ) or (res == QQ and K == RR):
            res = QQ
        else:
            if hasattr(res, 'intersection'):
                try:
                    res = res.intersection(K)
                except Exception:
                    pass
    return res

def conditions(witness):
    try:
        if isinstance(witness, dict):
            E = witness.get('E', None)
            K_list = witness.get('K_list', [])
            intersection = witness.get('intersection', None)
        elif isinstance(witness, (list, tuple)):
            E = witness[0]
            K_list = witness[1]
            intersection = witness[2] if len(witness) > 2 else None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: E is a field
    try:
        h1 = is_field(E)
    except Exception:
        h1 = False

    # H2: each K_i is an algebraically closed field
    try:
        h2 = True
        for K in K_list:
            if not (is_field(K) and is_alg_closed(K)):
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: The intersection is NOT an algebraically closed subfield of E
    try:
        if intersection is None:
            intersection = intersect_fields(K_list, E)
        
        is_alg_closed_subfield = is_alg_closed(intersection) and is_subfield(intersection, E)
        neg_q = not is_alg_closed_subfield
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is a field",
    "H_2: each K_i is an algebraically closed field",
    "¬Q: The intersection is not an algebraically closed subfield of E"
]

N_HYP = 2
NEG_Q_INDEX = 2