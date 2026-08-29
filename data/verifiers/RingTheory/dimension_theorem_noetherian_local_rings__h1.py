import sympy
from sympy import symbols

# Top-level setup
x, y, z = symbols('x y z')

def get_min_gens(obj):
    if isinstance(obj, dict):
        for k in ['min_gens_m_primary', 'm_primary_min_gens', 'min_gens']:
            if k in obj: 
                return obj[k]
    else:
        for k in ['min_gens_m_primary', 'm_primary_min_gens', 'min_gens']:
            if hasattr(obj, k): 
                return getattr(obj, k)
    return None

def get_krull_dim(obj):
    if isinstance(obj, dict):
        for k in ['krull_dimension', 'krull_dim', 'dim']:
            if k in obj: 
                return obj[k]
    else:
        for k in ['krull_dimension', 'krull_dim', 'dim']:
            if hasattr(obj, k): 
                return getattr(obj, k)
    return None

def conditions(witness) -> list[bool]:
    d, krull_dim, min_gens = None, None, None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], dict) or hasattr(witness[0], 'krull_dimension') or hasattr(witness[0], 'dim'):
                R, d = witness
            else:
                d, R = witness
            
            krull_dim = get_krull_dim(R)
            min_gens = get_min_gens(R)
            
        elif isinstance(witness, dict):
            if 'R' in witness and 'd' in witness:
                R = witness['R']
                d = witness['d']
                krull_dim = get_krull_dim(R)
                min_gens = get_min_gens(R)
            else:
                d = witness.get('d')
                krull_dim = get_krull_dim(witness)
                min_gens = get_min_gens(witness)
        else:
            d = getattr(witness, 'd', None)
            krull_dim = get_krull_dim(witness)
            min_gens = get_min_gens(witness)
    except Exception:
        pass

    try:
        h1 = (d is not None) and (krull_dim is not None) and (d == krull_dim)
    except Exception:
        h1 = False

    try:
        neg_q = (d is not None) and (min_gens is not None) and (d != min_gens)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: d is the Krull dimension of R",
    "¬Q: d is not equal to the minimum number of elements required to generate an m-primary ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1