import sympy
from sympy import ZZ, QQ, oo

# Top-level setup
Z = 'Z'
Q = 'Q'
Qx = 'Q[x]'
zero_mod = '0'
Z2 = 'Z/2Z'

def parse_module(M):
    if M in ('Z', sympy.ZZ, 'ZZ'): return 'Z'
    if M in ('Q', sympy.QQ, 'QQ'): return 'Q'
    if M in ('0', 0, 'zero', 'zero_mod', sympy.S.Zero): return '0'
    if M in ('Q[x]', 'Qx'): return 'Q[x]'
    if M in ('Z/2Z', 'Z2'): return 'Z/2Z'
    if M == sympy.oo or M == 'oo': return sympy.oo
    if isinstance(M, (int, sympy.Integer)): return int(M)
    return str(M)

def is_artinian(R, M):
    R_str = parse_module(R)
    M_str = parse_module(M)
    if R_str == 'Z':
        if M_str == '0': return True
        if M_str == 'Z': return False
        if M_str == 'Q': return False
        if M_str == 'Z/2Z': return True
    if R_str == 'Q':
        if M_str == '0': return True
        if M_str == 'Q': return True
        if M_str == 'Q[x]': return False
        if isinstance(M_str, int): return True
        if M_str == sympy.oo: return False
    return False

def to_dim(x):
    if x == '0': return 0
    return x

def is_exact(R, M_prime, M, M_double_prime):
    R_str = parse_module(R)
    Mp = parse_module(M_prime)
    M_str = parse_module(M)
    Mdp = parse_module(M_double_prime)
    
    if R_str == 'Z':
        valid_seqs = [
            ('Z', 'Z', '0'),
            ('0', 'Z', 'Z'),
            ('Z', 'Z', 'Z/2Z'),
            ('0', '0', '0')
        ]
        return (Mp, M_str, Mdp) in valid_seqs
    elif R_str == 'Q':
        valid_seqs = [
            ('Q', 'Q', '0'),
            ('0', 'Q', 'Q'),
            ('Q[x]', 'Q[x]', '0'),
            ('0', 'Q[x]', 'Q[x]'),
            ('0', '0', '0')
        ]
        if (Mp, M_str, Mdp) in valid_seqs:
            return True
            
        dim_p = to_dim(Mp)
        dim_m = to_dim(M_str)
        dim_dp = to_dim(Mdp)
        
        if isinstance(dim_p, int) and isinstance(dim_m, int) and isinstance(dim_dp, int):
            return dim_m == dim_p + dim_dp
        if dim_p == sympy.oo and dim_m == sympy.oo and dim_dp == 0:
            return True
        if dim_p == 0 and dim_m == sympy.oo and dim_dp == sympy.oo:
            return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R', witness.get('ring', 'Z'))
            M_prime = witness.get("M'", witness.get('M_prime', 'Z'))
            M = witness.get('M', 'Z')
            M_double_prime = witness.get("M''", witness.get('M_double_prime', '0'))
        elif hasattr(witness, 'R') and hasattr(witness, 'M'):
            R = witness.R
            M_prime = getattr(witness, 'M_prime', getattr(witness, "M'", 'Z'))
            M = witness.M
            M_double_prime = getattr(witness, 'M_double_prime', getattr(witness, "M''", '0'))
        elif isinstance(witness, (tuple, list)) and len(witness) >= 4:
            R, M_prime, M, M_double_prime = witness[:4]
        else:
            return [False, False, False, False]
            
        h1 = parse_module(R) in ('Z', 'Q')
        h2 = is_exact(R, M_prime, M, M_double_prime)
        h3 = is_artinian(R, M_double_prime)
        neg_q = not is_artinian(R, M)
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: 0 -> M' -> M -> M'' -> 0 is a short exact sequence of R-modules",
    "H_3: M'' is an Artinian R-module",
    "¬Q: M is not an Artinian R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3