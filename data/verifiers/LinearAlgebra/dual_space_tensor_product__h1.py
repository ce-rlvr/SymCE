import sympy
import math

# Top-level setup: named object bindings
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def parse_dim(d):
    if isinstance(d, str):
        if d.lower() in ['oo', 'inf', 'infinity']:
            return sympy.oo
        try:
            return int(d)
        except ValueError:
            return d
    return d

def get_dims(witness):
    dim_V, dim_W = None, None
    if isinstance(witness, dict):
        dim_V, dim_W = witness.get('dim_V'), witness.get('dim_W')
    elif hasattr(witness, 'dim_V') and hasattr(witness, 'dim_W'):
        dim_V, dim_W = witness.dim_V, witness.dim_W
    elif isinstance(witness, (list, tuple)) and len(witness) >= 2:
        dim_V, dim_W = witness[0], witness[1]
    
    return parse_dim(dim_V), parse_dim(dim_W)

def conditions(witness):
    try:
        dim_V, dim_W = get_dims(witness)
    except Exception:
        return [False, False]
        
    if dim_V is None or dim_W is None:
        return [False, False]
        
    # H1: W is a finite-dimensional vector space over F
    h1 = False
    try:
        if dim_W == sympy.oo or dim_W == math.inf:
            h1 = False
        else:
            h1 = bool(dim_W >= 0 and int(dim_W) == dim_W)
    except Exception:
        h1 = False
        
    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: There exists a natural isomorphism between (V \otimes W)* and V* \otimes W*
    # The natural map is an isomorphism if and only if at least one of V or W is finite-dimensional
    # (or if either is the zero vector space).
    neg_q = False
    try:
        is_finite_V = False
        if dim_V == sympy.oo or dim_V == math.inf:
            is_finite_V = False
        else:
            try:
                is_finite_V = bool(dim_V >= 0 and int(dim_V) == dim_V)
            except Exception:
                is_finite_V = False
                
        is_finite_W = h1
        
        is_iso = False
        if dim_V == 0 or dim_W == 0:
            is_iso = True
        else:
            is_iso = is_finite_V or is_finite_W
            
        neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: W is a finite-dimensional vector space over the field F",
    "¬Q: The natural map between (V \\otimes W)* and V* \\otimes W* is not an isomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1