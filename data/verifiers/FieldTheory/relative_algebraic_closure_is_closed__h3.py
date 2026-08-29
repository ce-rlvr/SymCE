import sympy
import sympy.polys

CC = sympy.S.Complexes
RR = sympy.S.Reals
QQ = sympy.S.Rationals

def is_field(F):
    if F in (QQ, RR, CC, 'QQ', 'RR', 'CC', 'Q', 'R', 'C', 'Rationals', 'Reals', 'Complexes'):
        return True
    if hasattr(F, 'is_Field') and F.is_Field:
        return True
    if hasattr(F, 'is_field') and F.is_field:
        return True
    try:
        if F in (sympy.polys.domains.QQ, sympy.polys.domains.RR, sympy.polys.domains.CC):
            return True
    except Exception:
        pass
    return False

def is_alg_closed(F):
    if F in (CC, 'CC', 'C', 'Complexes'):
        return True
    try:
        if F == sympy.polys.domains.CC:
            return True
    except Exception:
        pass
    return False

def is_subfield(K, L):
    if not (is_field(K) and is_field(L)):
        return False
    
    def level(F):
        if F in (QQ, 'QQ', 'Q', 'Rationals'): return 1
        if F in (RR, 'RR', 'R', 'Reals'): return 2
        if F in (CC, 'CC', 'C', 'Complexes'): return 3
        try:
            if F == sympy.polys.domains.QQ: return 1
            if F == sympy.polys.domains.RR: return 2
            if F == sympy.polys.domains.CC: return 3
        except Exception:
            pass
        return 0
        
    lK = level(K)
    lL = level(L)
    
    if lK > 0 and lL > 0:
        return lK <= lL
        
    if K == L:
        return True
        
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            L = witness.get('L')
            K = witness.get('K')
            E = witness.get('E')
        else:
            L, K, E = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(is_field(L) and is_alg_closed(L))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(is_subfield(K, L))
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not (is_field(E) and is_alg_closed(E))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: L is an algebraically closed field",
    "H_2: K is a subfield of L",
    "¬Q: E is not an algebraically closed field"
]

N_HYP = 2
NEG_Q_INDEX = 2