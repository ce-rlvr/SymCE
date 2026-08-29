import sympy
from sympy.polys.domains import QQ, ZZ, GF, RR, CC
from sympy import Symbol, sqrt, I

x = Symbol('x')

def _get_char_and_prime_subfield(K):
    char = None
    if hasattr(K, 'characteristic'):
        char_attr = K.characteristic
        char = char_attr() if callable(char_attr) else char_attr
    elif K == QQ:
        char = 0
    elif hasattr(K, 'mod'):
        char = K.mod
    elif hasattr(K, 'p'):
        char = K.p
    else:
        char = 0
        
    try:
        P = QQ if char == 0 else GF(char)
    except Exception:
        P = None
    return char, P

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) != 2:
                K, P = None, None
            else:
                K, P = witness
        else:
            K = witness
            _, P = _get_char_and_prime_subfield(K)
            
        h1 = False
        if K is not None and P is not None:
            if getattr(K, 'is_Field', False) and getattr(P, 'is_Field', False):
                char, expected_P = _get_char_and_prime_subfield(K)
                if P == expected_P:
                    h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if isinstance(witness, tuple):
            if len(witness) == 2:
                K, P = witness
            else:
                K, P = None, None
        else:
            K = witness
            _, P = _get_char_and_prime_subfield(K)
            
        if K is not None and P is not None:
            def check_fg(ring, base):
                seen = set()
                while ring not in seen:
                    if ring == base:
                        return True
                    seen.add(ring)
                    if hasattr(ring, 'domain') and ring.domain is not None:
                        ring = ring.domain
                    else:
                        break
                return False
            
            neg_q = check_fg(K, P)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is the prime subfield of K",
    "¬Q: K is finitely generated as a field extension over P"
]

N_HYP = 1
NEG_Q_INDEX = 1