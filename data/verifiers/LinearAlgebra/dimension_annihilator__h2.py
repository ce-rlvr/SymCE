import sympy
from sympy import Symbol, oo, Matrix, eye, zeros

# Top-level setup
aleph_0 = Symbol('aleph_0')
aleph_1 = Symbol('aleph_1')
c = Symbol('c')

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: W is a subspace of V",
    "¬Q: dim(W) + dim(W^0) != dim(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_valid_dim(d):
    if isinstance(d, (int, sympy.Integer)):
        return d >= 0
    if d == oo:
        return True
    if isinstance(d, Symbol) and d.name in ['aleph_0', 'aleph_1', 'c']:
        return True
    return False

def is_subspace_dim(dim_W, dim_V):
    if not is_valid_dim(dim_W):
        return False
    if isinstance(dim_W, (int, sympy.Integer)) and isinstance(dim_V, (int, sympy.Integer)):
        return dim_W <= dim_V
    if isinstance(dim_V, Symbol) and dim_V.name == 'aleph_0':
        if isinstance(dim_W, Symbol) and dim_W.name in ['aleph_1', 'c']:
            return False
    return True

def is_valid_annihilator_dim(dim_V, dim_W, dim_W0):
    if isinstance(dim_V, (int, sympy.Integer)) and isinstance(dim_W, (int, sympy.Integer)):
        if isinstance(dim_W0, (int, sympy.Integer)):
            return dim_W0 == dim_V - dim_W
        return False
    return is_valid_dim(dim_W0)

def extract_dims(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            return witness
        if len(witness) == 2:
            dim_V, dim_W = witness
            if isinstance(dim_V, Symbol) and dim_V.name == 'aleph_0' and dim_W == 0:
                return aleph_0, 0, c
            if isinstance(dim_V, (int, sympy.Integer)) and isinstance(dim_W, (int, sympy.Integer)):
                return dim_V, dim_W, dim_V - dim_W
                
    if isinstance(witness, dict):
        if 'dim_V' in witness and 'dim_W' in witness and 'dim_W0' in witness:
            return witness['dim_V'], witness['dim_W'], witness['dim_W0']
            
    if hasattr(witness, 'dim_V') and hasattr(witness, 'dim_W') and hasattr(witness, 'dim_W0'):
        return witness.dim_V, witness.dim_W, witness.dim_W0
        
    if isinstance(witness, str):
        s = witness.lower()
        if any(kw in s for kw in ['inf', 'poly', 'f[x]', 'sequence', 'r[x]', 'c[x]', 'function', 'l2', 'hilbert', 'banach']):
            return aleph_0, 0, c
            
    if isinstance(witness, Matrix):
        n = witness.rows
        r = witness.rank()
        return n, r, n - r
        
    if isinstance(witness, list) and len(witness) > 0 and all(isinstance(v, Matrix) for v in witness):
        try:
            M = Matrix.hstack(*witness)
            n = M.rows
            r = M.rank()
            return n, r, n - r
        except Exception:
            pass
            
    return None, None, None

def conditions(witness) -> list[bool]:
    dim_V, dim_W, dim_W0 = extract_dims(witness)
    
    if dim_V is None:
        return [False, False, False]
        
    try:
        h1 = is_valid_dim(dim_V)
    except Exception:
        h1 = False
        
    try:
        h2 = is_subspace_dim(dim_W, dim_V) and is_valid_annihilator_dim(dim_V, dim_W, dim_W0)
    except Exception:
        h2 = False
        
    try:
        sum_dim = dim_W + dim_W0
        neg_q = (sum_dim != dim_V)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]