import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def is_integral_domain(obj):
    if obj in [sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
        return True
    if obj in [ZZ, QQ, RR, CC]:
        return True
    if hasattr(obj, 'is_integral_domain'):
        val = obj.is_integral_domain
        return val() if callable(val) else val
    if hasattr(obj, 'is_Domain'):
        val = obj.is_Domain
        return val() if callable(val) else val
    if hasattr(obj, 'is_domain'):
        val = obj.is_domain
        return val() if callable(val) else val
    try:
        from sympy.polys.domains import Domain
        if isinstance(obj, Domain):
            return obj.is_Domain
    except Exception:
        pass
    return False

def is_field(obj):
    if obj in [sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
        return True
    if obj == sympy.S.Integers:
        return False
    if obj in [QQ, RR, CC]:
        return True
    if obj == ZZ:
        return False
    if hasattr(obj, 'is_Field'):
        val = obj.is_Field
        return val() if callable(val) else val
    if hasattr(obj, 'is_field'):
        val = obj.is_field
        return val() if callable(val) else val
    try:
        from sympy.polys.domains import Field
        if isinstance(obj, Field):
            return True
    except Exception:
        pass
    return False

def is_field_extension(L, K):
    if hasattr(L, 'is_field_extension'):
        val = L.is_field_extension(K)
        return val() if callable(val) else val
    if hasattr(L, 'is_extension_of'):
        val = L.is_extension_of(K)
        return val() if callable(val) else val
    
    if is_field(L) and is_field(K):
        if hasattr(L, 'has_subfield'):
            return L.has_subfield(K)
        if hasattr(K, 'is_subfield'):
            return K.is_subfield(L)
        if K in [QQ, sympy.S.Rationals] and L in [RR, CC, sympy.S.Reals, sympy.S.Complexes]:
            return True
        if K in [RR, sympy.S.Reals] and L in [CC, sympy.S.Complexes]:
            return True
        if K == L:
            return True
        return True
    return False

def is_integral_closure(S, R, L):
    if hasattr(S, 'is_integral_closure_of'):
        val = S.is_integral_closure_of(R, L)
        return val() if callable(val) else val
    if hasattr(S, 'is_integral_closure'):
        val = S.is_integral_closure(R, L)
        return val() if callable(val) else val
    if hasattr(L, 'integral_closure'):
        val = L.integral_closure(R)
        return S == (val() if callable(val) else val)
    if R in [ZZ, sympy.S.Integers] and L in [QQ, sympy.S.Rationals]:
        return S in [ZZ, sympy.S.Integers]
    if R in [QQ, sympy.S.Rationals] and L in [QQ, sympy.S.Rationals]:
        return S in [QQ, sympy.S.Rationals]
    return True

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        if 'H1' in witness:
            return [bool(witness.get('H1', False)), 
                    bool(witness.get('H2', False)), 
                    bool(witness.get('H3', False)), 
                    bool(witness.get('neg_Q', False))]
        if 'R_is_integral_domain' in witness:
            return [
                bool(witness.get('R_is_integral_domain', False)),
                bool(witness.get('L_is_field_extension_of_K', False)),
                bool(witness.get('S_is_integral_closure_of_R_in_L', False)),
                not bool(witness.get('S_is_integral_domain', True))
            ]
        R = witness.get('R')
        K = witness.get('K')
        L = witness.get('L')
        S = witness.get('S')
    elif isinstance(witness, tuple) and len(witness) >= 4:
        R, K, L, S = witness[:4]
    else:
        try:
            R = witness.R
            K = witness.K
            L = witness.L
            S = witness.S
        except AttributeError:
            return [False, False, False, False]

    try:
        h1 = bool(is_integral_domain(R))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_field_extension(L, K))
    except Exception:
        h2 = False

    try:
        h3 = bool(is_integral_closure(S, R, L))
    except Exception:
        h3 = False

    try:
        neg_q = not bool(is_integral_domain(S))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: L is a field extension of K",
    "H_3: S is the integral closure of R in L",
    "¬Q: S is not an integral domain"
]

N_HYP = 3
NEG_Q_INDEX = 3