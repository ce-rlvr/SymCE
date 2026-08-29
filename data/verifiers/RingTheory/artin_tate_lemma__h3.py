import sympy
from sympy.abc import x

# Top-level setup: named object bindings that the witness expression may reference.
ZZ = sympy.ZZ
QQ = sympy.QQ
Z_poly = sympy.polys.domains.ZZ.poly_ring(x)
Q_poly = sympy.polys.domains.QQ.poly_ring(x)
Qx = sympy.polys.domains.QQ.frac_field(x)

def normalize_ring(ring):
    """
    Map the provided ring object or string to a known standard ring identifier.
    This allows robust checking of algebraic properties that SymPy cannot natively compute.
    """
    try:
        if ring == ZZ or ring == sympy.polys.domains.ZZ:
            return 'ZZ'
        if ring == QQ or ring == sympy.polys.domains.QQ:
            return 'QQ'
        if ring == Z_poly:
            return 'Z_poly'
        if ring == Q_poly:
            return 'Q_poly'
        if ring == Qx:
            return 'Qx'
    except Exception:
        pass
        
    try:
        s = str(ring)
        s_lower = s.lower()
    except Exception:
        return 'unknown'
        
    if s in ('ZZ', 'Integers', 'S.Integers', 'ZZ_domain', 'Z'):
        return 'ZZ'
    if s in ('QQ', 'Rationals', 'S.Rationals', 'QQ_domain', 'Q', 'k', 'K', 'RR', 'Reals', 'CC', 'Complexes', 'R', 'C'):
        return 'QQ'
        
    if 'inf' in s_lower or 'x_1' in s_lower or 'x1' in s_lower or '...' in s_lower:
        return 'Q_inf_poly'
        
    if 'series' in s_lower or '[[x]]' in s_lower:
        return 'Q_series'
        
    if 'frac' in s_lower or '(x' in s_lower:
        return 'Qx'
        
    if 'poly' in s_lower or '[x' in s_lower:
        if 'zz' in s_lower or 'integers' in s_lower or 'z' in s_lower:
            return 'Z_poly'
        return 'Q_poly'
        
    if 'gf' in s_lower or 'finitefield' in s_lower or 'f_p' in s_lower or 'fp' in s_lower or 'field' in s_lower:
        return 'QQ'
        
    return s

def is_comm_ring(r):
    return r in ('ZZ', 'QQ', 'Qx', 'Q_poly', 'Z_poly', 'Q_series', 'Q_inf_poly')

def is_subset(A, B):
    if A == B:
        return True
    subs = {
        'ZZ': ['QQ', 'Z_poly', 'Q_poly', 'Qx', 'Q_series', 'Q_inf_poly'],
        'QQ': ['Q_poly', 'Qx', 'Q_series', 'Q_inf_poly'],
        'Z_poly': ['Q_poly', 'Qx', 'Q_series', 'Q_inf_poly'],
        'Q_poly': ['Qx', 'Q_series', 'Q_inf_poly']
    }
    return B in subs.get(A, [])

def is_noetherian(r):
    return r in ('ZZ', 'QQ', 'Q_poly', 'Qx', 'Z_poly', 'Q_series')

def is_fg_module(base, top):
    if base == top:
        return True
    return False

def is_fg_algebra(base, top):
    if base == top:
        return True
    if base == 'QQ' and top == 'Q_poly':
        return True
    if base == 'ZZ' and top == 'Z_poly':
        return True
    return False

def conditions(witness) -> list[bool]:
    # Allow witness to be a dictionary mapping to the rings
    if isinstance(witness, dict):
        try:
            R_raw = witness.get('R', witness.get('R_ring', witness.get('r')))
            S_raw = witness.get('S', witness.get('S_ring', witness.get('s')))
            T_raw = witness.get('T', witness.get('T_ring', witness.get('t')))
            if R_raw is not None and S_raw is not None and T_raw is not None:
                witness = (R_raw, S_raw, T_raw)
        except Exception:
            pass

    try:
        if len(witness) != 3:
            return [False, False, False, False]
        R_raw, S_raw, T_raw = witness
    except Exception:
        return [False, False, False, False]
        
    R = normalize_ring(R_raw)
    S = normalize_ring(S_raw)
    T = normalize_ring(T_raw)
    
    # H_1: R, S, T are commutative rings such that R <= S <= T
    try:
        h1 = is_comm_ring(R) and is_comm_ring(S) and is_comm_ring(T) and is_subset(R, S) and is_subset(S, T)
    except Exception:
        h1 = False

    # H_2: R is a Noetherian ring
    try:
        h2 = is_noetherian(R)
    except Exception:
        h2 = False

    # H_3: T is finitely generated as a module over S
    try:
        h3 = is_fg_module(S, T)
    except Exception:
        h3 = False

    # ¬Q: S is NOT finitely generated as an algebra over R
    try:
        neg_q = not is_fg_algebra(R, S)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R, S, T are commutative rings such that R <= S <= T",
    "H_2: R is a Noetherian ring",
    "H_3: T is finitely generated as a module over S",
    "¬Q: S is NOT finitely generated as an algebra over R"
]

N_HYP = 3
NEG_Q_INDEX = 3