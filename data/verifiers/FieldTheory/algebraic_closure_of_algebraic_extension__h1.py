import sympy
from sympy import S, Symbol

# Top-level setup
Q = S.Rationals
R = S.Reals
C = S.Complexes
Q_bar = Symbol('Q_bar')
QQ = Symbol('QQ')
RR = Symbol('RR')
CC = Symbol('CC')
QQ_bar = Symbol('QQ_bar')

def get_name(f):
    if isinstance(f, str): 
        return f
    if hasattr(f, 'name') and isinstance(f.name, str): 
        return f.name
    if f == S.Rationals: 
        return 'Q'
    if f == S.Reals: 
        return 'R'
    if f == S.Complexes: 
        return 'C'
    s = str(f)
    if s in ['QQ', 'RR', 'CC']: 
        return s[0]
    if 'AlgebraicNumbers' in s: 
        return 'Q_bar'
    if s == 'QQ(x)': 
        return 'Q(x)'
    if s == 'CC(x)': 
        return 'C(x)'
    return s

def is_same_field(f1, f2):
    if f1 is None or f2 is None: 
        return False
    n1 = get_name(f1)
    n2 = get_name(f2)
    if n1 == n2: 
        return True
    if n1 in ['Q_bar', 'QQ_bar', 'AlgebraicNumbers'] and n2 in ['Q_bar', 'QQ_bar', 'AlgebraicNumbers']: 
        return True
    if n1 in ['C', 'CC'] and n2 in ['C', 'CC']: 
        return True
    if n1 in ['R', 'RR'] and n2 in ['R', 'RR']: 
        return True
    if n1 in ['Q', 'QQ'] and n2 in ['Q', 'QQ']: 
        return True
    return False

def is_alg_closed(f):
    name = get_name(f)
    return is_same_field(name, 'C') or is_same_field(name, 'Q_bar') or name in ['C(x)_bar', 'Q(x)_bar']

def contains(sup, sub):
    if is_same_field(sup, sub): 
        return True
    sup_name = get_name(sup)
    sub_name = get_name(sub)
    
    if is_same_field(sup_name, 'C'):
        return is_same_field(sub_name, 'Q') or is_same_field(sub_name, 'R') or is_same_field(sub_name, 'Q_bar')
    if is_same_field(sup_name, 'R'):
        return is_same_field(sub_name, 'Q')
    if is_same_field(sup_name, 'Q_bar'):
        return is_same_field(sub_name, 'Q')
    if sup_name == 'C(x)_bar':
        return sub_name == 'C(x)' or is_same_field(sub_name, 'C') or is_same_field(sub_name, 'Q') or is_same_field(sub_name, 'R') or is_same_field(sub_name, 'Q_bar')
    if sup_name == 'Q(x)_bar':
        return sub_name == 'Q(x)' or is_same_field(sub_name, 'Q')
    return False

def alg_closure_in(sub, omega):
    if not contains(omega, sub):
        return None
    sup_name = get_name(omega)
    sub_name = get_name(sub)
    
    if is_same_field(sup_name, 'C'):
        if is_same_field(sub_name, 'Q'): return 'Q_bar'
        if is_same_field(sub_name, 'R'): return 'C'
        if is_same_field(sub_name, 'C'): return 'C'
        if is_same_field(sub_name, 'Q_bar'): return 'Q_bar'
        
    if is_same_field(sup_name, 'Q_bar'):
        if is_same_field(sub_name, 'Q'): return 'Q_bar'
        if is_same_field(sub_name, 'Q_bar'): return 'Q_bar'
        
    if sup_name == 'C(x)_bar':
        if sub_name == 'C(x)': return 'C(x)_bar'
        if is_same_field(sub_name, 'C'): return 'C'
        if is_same_field(sub_name, 'Q'): return 'Q_bar'
        if is_same_field(sub_name, 'R'): return 'C'
        if is_same_field(sub_name, 'Q_bar'): return 'Q_bar'
        
    if sup_name == 'Q(x)_bar':
        if sub_name == 'Q(x)': return 'Q(x)_bar'
        if is_same_field(sub_name, 'Q'): return 'Q_bar'
        
    return None

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 5:
            return [False, False, False, False]
        F, E, Omega, A_F, A_E = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: Omega is an algebraically closed field containing E
    try:
        h1 = is_alg_closed(Omega) and contains(Omega, E)
    except Exception:
        h1 = False
        
    # H_2: A_F is the algebraic closure of F in Omega
    try:
        expected_A_F = alg_closure_in(F, Omega)
        h2 = is_same_field(A_F, expected_A_F) if expected_A_F else False
    except Exception:
        h2 = False
        
    # H_3: A_E is the algebraic closure of E in Omega
    try:
        expected_A_E = alg_closure_in(E, Omega)
        h3 = is_same_field(A_E, expected_A_E) if expected_A_E else False
    except Exception:
        h3 = False
        
    # neg_Q: A_F != A_E
    try:
        neg_q = not is_same_field(A_F, A_E)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Omega is an algebraically closed field containing E",
    "H_2: A_F is the algebraic closure of F in Omega",
    "H_3: A_E is the algebraic closure of E in Omega",
    "¬Q: A_F != A_E"
]

N_HYP = 3
NEG_Q_INDEX = 3