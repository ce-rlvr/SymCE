import sympy

class RingObj:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

# Top-level setup: named object bindings for the witness expression
Z = RingObj('Z')
Q = RingObj('Q')
Z_x = RingObj('Z[x]')
Q_x = RingObj('Q[x]')
Q_x_frac = RingObj('Q(x)')
Q_x_y = RingObj('Q[x,y]')
Q_x_y_frac = RingObj('Q(x,y)')
k_x_y = RingObj('k[x,y]')
k_x_y_frac = RingObj('k(x,y)')
k_x = RingObj('k[x]')
k_x_frac = RingObj('k(x)')
Z_x_y = RingObj('Z[x,y]')
Z_i = RingObj('Z[i]')
Q_i = RingObj('Q(i)')

# Properties of various rings and fields
rings = {
    'Z': {'comm': True, 'noeth': True, 'domain': True, 'dim': 1, 'frac': 'Q'},
    'Q': {'comm': True, 'noeth': True, 'domain': True, 'dim': 0, 'frac': 'Q'},
    'Z[x]': {'comm': True, 'noeth': True, 'domain': True, 'dim': 2, 'frac': 'Q(x)'},
    'Q[x]': {'comm': True, 'noeth': True, 'domain': True, 'dim': 1, 'frac': 'Q(x)'},
    'Q(x)': {'comm': True, 'noeth': True, 'domain': True, 'dim': 0, 'frac': 'Q(x)'},
    'Q[x,y]': {'comm': True, 'noeth': True, 'domain': True, 'dim': 2, 'frac': 'Q(x,y)'},
    'Q(x,y)': {'comm': True, 'noeth': True, 'domain': True, 'dim': 0, 'frac': 'Q(x,y)'},
    'k[x,y]': {'comm': True, 'noeth': True, 'domain': True, 'dim': 2, 'frac': 'k(x,y)'},
    'k(x,y)': {'comm': True, 'noeth': True, 'domain': True, 'dim': 0, 'frac': 'k(x,y)'},
    'k[x]': {'comm': True, 'noeth': True, 'domain': True, 'dim': 1, 'frac': 'k(x)'},
    'k(x)': {'comm': True, 'noeth': True, 'domain': True, 'dim': 0, 'frac': 'k(x)'},
    'Z[x,y]': {'comm': True, 'noeth': True, 'domain': True, 'dim': 3, 'frac': 'Q(x,y)'},
    'Z[i]': {'comm': True, 'noeth': True, 'domain': True, 'dim': 1, 'frac': 'Q(i)'},
    'Q(i)': {'comm': True, 'noeth': True, 'domain': True, 'dim': 0, 'frac': 'Q(i)'},
}

# Known finite algebraic field extensions (K, L)
finite_extensions = {
    ('Q', 'Q'): True,
    ('Q', 'Q(i)'): True,
    ('Q(i)', 'Q(i)'): True,
    ('Q(x)', 'Q(x)'): True,
    ('Q(x,y)', 'Q(x,y)'): True,
    ('k(x,y)', 'k(x,y)'): True,
    ('k(x)', 'k(x)'): True,
}

# Known subring relationships (Subring, Superring)
subrings = {
    ('Z', 'Z'): True,
    ('Z', 'Q'): True,
    ('Z', 'Z[i]'): True,
    ('Z[i]', 'Z[i]'): True,
    ('Z[i]', 'Q(i)'): True,
    ('Q', 'Q(i)'): True,
    ('Z[x]', 'Z[x]'): True,
    ('Z[x]', 'Q(x)'): True,
    ('Z[x]', 'Q[x]'): True,
    ('Z', 'Z[x]'): True,
    ('Q', 'Q'): True,
    ('Q', 'Q[x]'): True,
    ('Q', 'Q(x)'): True,
    ('Q[x]', 'Q[x]'): True,
    ('Q[x]', 'Q(x)'): True,
    ('Q[x]', 'Q[x,y]'): True,
    ('Q(x)', 'Q(x)'): True,
    ('Q(x)', 'Q(x,y)'): True,
    ('Q[x,y]', 'Q[x,y]'): True,
    ('Q[x,y]', 'Q(x,y)'): True,
    ('Q(x,y)', 'Q(x,y)'): True,
    ('k[x,y]', 'k[x,y]'): True,
    ('k[x,y]', 'k(x,y)'): True,
    ('k(x,y)', 'k(x,y)'): True,
    ('k[x]', 'k[x]'): True,
    ('k[x]', 'k(x)'): True,
    ('k[x]', 'k[x,y]'): True,
    ('k(x)', 'k(x)'): True,
    ('k(x)', 'k(x,y)'): True,
    ('Z[x,y]', 'Z[x,y]'): True,
    ('Z[x,y]', 'Q(x,y)'): True,
}

def conditions(witness):
    """
    Given a witness tuple (R, K, L, S), checks whether it is a valid counterexample
    to the false Krull-Akizuki conjecture.
    """
    try:
        R, K, L, S = witness
    except Exception:
        return [False, False, False, False, False]
        
    def get_name(obj):
        if hasattr(obj, 'name'):
            return obj.name
        return str(obj)
        
    try:
        R_name = get_name(R)
        K_name = get_name(K)
        L_name = get_name(L)
        S_name = get_name(S)
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: R is a commutative Noetherian integral domain
    try:
        h1 = rings[R_name]['comm'] and rings[R_name]['noeth'] and rings[R_name]['domain']
    except Exception:
        h1 = False
        
    # H_2: K is the field of fractions of R
    try:
        h2 = rings[R_name]['frac'] == K_name
    except Exception:
        h2 = False
        
    # H_3: L is a finite algebraic field extension of K
    try:
        h3 = finite_extensions.get((K_name, L_name), False)
    except Exception:
        h3 = False
        
    # H_4: S is a subring of L such that R \subseteq S \subseteq L
    try:
        h4 = subrings.get((R_name, S_name), False) and subrings.get((S_name, L_name), False)
    except Exception:
        h4 = False
        
    # ¬Q: S is NOT a one-dimensional Noetherian ring
    try:
        is_one_dim_noeth = rings[S_name]['dim'] == 1 and rings[S_name]['noeth']
        neg_q = not is_one_dim_noeth
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: L is a finite algebraic field extension of K",
    "H_4: S is a subring of L such that R \\subseteq S \\subseteq L",
    "¬Q: S is not a one-dimensional Noetherian ring"
]

N_HYP = 4
NEG_Q_INDEX = 4