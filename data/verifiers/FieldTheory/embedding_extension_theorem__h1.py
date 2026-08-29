import sympy
import math
import itertools
import functools

# Top-level setup
x, y, t = sympy.symbols('x y t')

def is_alg_closed(field):
    return field in ['Q_bar', 'C', 'Fp_bar']

def is_extension(sub, sup):
    if sub == sup:
        return True
    extensions = {
        'Q': ['Q_bar', 'R', 'C', 'Q(t)', 'C(t)'],
        'Q_bar': ['C', 'C(t)'],
        'R': ['C', 'C(t)'],
        'C': ['C(t)'],
        'Q(t)': ['C(t)'],
        'Fp': ['Fp_bar', 'Fp(t)'],
        'Fp_bar': [],
        'Fp(t)': [],
        'C(t)': []
    }
    return sup in extensions.get(sub, [])

def is_algebraic_extension(sub, sup):
    if not is_extension(sub, sup):
        return False
    if sub == sup:
        return True
    alg_exts = {
        'Q': ['Q_bar'],
        'R': ['C'],
        'Fp': ['Fp_bar']
    }
    return sup in alg_exts.get(sub, [])

def tr_deg_over(sup, sub):
    if not is_extension(sub, sup):
        return None
    if is_algebraic_extension(sub, sup):
        return 0
    
    tr_degs = {
        ('Q', 'R'): float('inf'),
        ('Q', 'C'): float('inf'),
        ('Q', 'Q(t)'): 1,
        ('Q', 'C(t)'): float('inf'),
        ('Q_bar', 'C'): float('inf'),
        ('Q_bar', 'C(t)'): float('inf'),
        ('R', 'C(t)'): 1,
        ('C', 'C(t)'): 1,
        ('Q(t)', 'C(t)'): float('inf'),
        ('Fp', 'Fp(t)'): 1
    }
    return tr_degs.get((sub, sup), None)

def is_embeddable(F, L):
    chars = {
        'Q': 0, 'Q_bar': 0, 'R': 0, 'C': 0, 'Q(t)': 0, 'C(t)': 0,
        'Fp': 'p', 'Fp_bar': 'p', 'Fp(t)': 'p'
    }
    if F not in chars or L not in chars:
        return False
    if chars[F] != chars[L]:
        return False
        
    reals = {'Q': True, 'R': True, 'Q(t)': True, 
             'Q_bar': False, 'C': False, 'C(t)': False,
             'Fp': False, 'Fp_bar': False, 'Fp(t)': False}
    if not reals[F] and reals[L]:
        return False
        
    tr_deg_prime = {
        'Q': 0, 'Q_bar': 0, 'R': float('inf'), 'C': float('inf'),
        'Q(t)': 1, 'C(t)': float('inf'),
        'Fp': 0, 'Fp_bar': 0, 'Fp(t)': 1
    }
    if tr_deg_prime[F] > tr_deg_prime[L]:
        return False
        
    return True

def conditions(witness) -> list[bool]:
    """
    Expected witness format:
    A dictionary {'F': 'Q', 'E': 'Q(t)', 'L': 'Q_bar', 'sigma': 'inclusion'}
    or a tuple ('Q', 'Q(t)', 'Q_bar', 'inclusion')
    Supported fields: 'Q', 'Q_bar', 'R', 'C', 'Q(t)', 'C(t)', 'Fp', 'Fp_bar', 'Fp(t)'
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            E = witness.get('E')
            L = witness.get('L')
            sigma = witness.get('sigma', 'inclusion')
        else:
            F, E, L, sigma = witness
            
        # H1: L is an algebraically closed field
        try:
            h1 = is_alg_closed(L)
        except Exception:
            h1 = False
            
        # H2: sigma: F -> L is a field embedding
        try:
            h2 = is_embeddable(F, L) and is_extension(F, E)
        except Exception:
            h2 = False
            
        # neg_Q: There does NOT exist an embedding E -> L extending sigma
        try:
            deg_E = tr_deg_over(E, F)
            deg_L = tr_deg_over(L, F)
            
            if deg_E is None or deg_L is None:
                neg_q = False
            else:
                neg_q = deg_E > deg_L
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L is an algebraically closed field",
    "H_2: \\sigma: F \\to L is a field embedding",
    "¬Q: There does not exist a field embedding \\tilde{\\sigma}: E \\to L extending \\sigma"
]

N_HYP = 2
NEG_Q_INDEX = 2