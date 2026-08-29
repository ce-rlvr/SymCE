import sympy
from sympy import QQ, RR, CC, ZZ
from sympy.ntheory import isprime

# Top-level setup
Q = 'Q'
R = 'R'
C = 'C'
Q_bar = 'Q_bar'
F2 = 'F2'
F2_bar = 'F2_bar'
F3 = 'F3'
F3_bar = 'F3_bar'
F5 = 'F5'
F5_bar = 'F5_bar'
Z = 'Z'
N = 'N'

def map_to_string(obj):
    if isinstance(obj, str):
        return obj
    s = str(obj)
    mapping = {
        'QQ': 'Q',
        'Rationals': 'Q',
        'RR': 'R',
        'Reals': 'R',
        'CC': 'C',
        'Complexes': 'C',
        'AlgebraicNumbers': 'Q_bar',
        'QQ_bar': 'Q_bar',
        'ZZ': 'Z',
        'Integers': 'Z',
        'NN': 'N',
        'Naturals': 'N'
    }
    return mapping.get(s, obj)

def is_finite_field_str(s):
    if s.startswith('F'):
        rest = s[1:]
        if rest.endswith('_bar'):
            rest = rest[:-4]
        if rest.isdigit():
            return isprime(int(rest))
    return False

def is_field(K):
    if hasattr(K, 'is_field') and callable(K.is_field):
        try: 
            return bool(K.is_field())
        except Exception: 
            pass
    if hasattr(K, 'is_Field'):
        try: 
            return bool(K.is_Field)
        except Exception: 
            pass
    if isinstance(K, str):
        if K in {'Q', 'R', 'C', 'Q_bar'}:
            return True
        return is_finite_field_str(K)
    return False

def is_alg_closure(K, F):
    if hasattr(K, 'is_algebraic_closure_of') and callable(K.is_algebraic_closure_of):
        try: 
            return bool(K.is_algebraic_closure_of(F))
        except Exception: 
            pass
    if isinstance(F, str) and isinstance(K, str):
        if not (is_field(F) and is_field(K)):
            return False
        closures = {
            'Q': 'Q_bar',
            'R': 'C',
            'C': 'C',
            'Q_bar': 'Q_bar',
        }
        if F in closures:
            return closures[F] == K
        
        if is_finite_field_str(F) and is_finite_field_str(K):
            p_F = F[1:].replace('_bar', '')
            p_K = K[1:].replace('_bar', '')
            return p_F == p_K and K.endswith('_bar')
    return False

def is_F_isomorphic(K1, K2, F):
    if hasattr(K1, 'is_isomorphic_to') and callable(K1.is_isomorphic_to):
        try:
            return bool(K1.is_isomorphic_to(K2, F))
        except Exception:
            pass
    if isinstance(K1, str) and isinstance(K2, str):
        if not (is_field(K1) and is_field(K2) and is_field(F)):
            return False
        return K1 == K2
    return K1 == K2

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        F_obj, K1_obj, K2_obj = witness
    except Exception:
        return [False, False, False]
    
    F_str = map_to_string(F_obj)
    K1_str = map_to_string(K1_obj)
    K2_str = map_to_string(K2_obj)
    
    try:
        h1 = is_field(F_str)
    except Exception:
        h1 = False
        
    try:
        h2 = is_alg_closure(K1_str, F_str)
    except Exception:
        h2 = False
        
    try:
        q = is_F_isomorphic(K1_str, K2_str, F_str)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K1 is an algebraic closure of F",
    "¬Q: There does not exist a field isomorphism φ: K1 → K2 such that φ(x) = x for all x in F"
]

N_HYP = 2
NEG_Q_INDEX = 2