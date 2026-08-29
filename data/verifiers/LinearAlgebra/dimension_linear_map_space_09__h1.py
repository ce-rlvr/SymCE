import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is finite-dimensional",
    "H_2: W is finite-dimensional",
    "¬Q: dim(L(V, W)) != dim(V) * dim(W)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def extract_dim(obj):
    if obj is None:
        return None
        
    def get_int(val):
        if isinstance(val, bool):
            return None
        if isinstance(val, int):
            return val
        if hasattr(val, 'is_integer'):
            is_int = False
            if callable(val.is_integer):
                try:
                    is_int = val.is_integer()
                except Exception:
                    pass
            else:
                is_int = bool(val.is_integer)
            if is_int:
                return int(val)
        return None

    res = get_int(obj)
    if res is not None:
        return res
        
    d = None
    if hasattr(obj, 'dim'):
        d = obj.dim
    elif hasattr(obj, 'dimension'):
        d = obj.dimension
    elif isinstance(obj, dict) and 'dim' in obj:
        d = obj['dim']
    elif hasattr(obj, 'shape') and isinstance(obj.shape, tuple) and len(obj.shape) > 0:
        d = obj.shape[0]
    elif isinstance(obj, (list, tuple)) and len(obj) == 2 and isinstance(obj[1], int):
        d = obj[1]
        
    return get_int(d)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        dim_V = None
        dim_W = None
        dim_L = None
        
        if isinstance(witness, (list, tuple)) and len(witness) == 3:
            v, w, l = witness
            dim_V = extract_dim(v)
            dim_W = extract_dim(w)
            dim_L = extract_dim(l)
            
        elif isinstance(witness, dict):
            dim_V = extract_dim(witness.get('dim_V'))
            if dim_V is None: 
                dim_V = extract_dim(witness.get('V'))
            
            dim_W = extract_dim(witness.get('dim_W'))
            if dim_W is None: 
                dim_W = extract_dim(witness.get('W'))
            
            dim_L = extract_dim(witness.get('dim_L'))
            if dim_L is None: 
                dim_L = extract_dim(witness.get('L'))
            
            if dim_V is None:
                for k, val in witness.items():
                    if isinstance(k, str) and 'V' in k:
                        dim_V = extract_dim(val)
                        if dim_V is not None: break
            if dim_W is None:
                for k, val in witness.items():
                    if isinstance(k, str) and 'W' in k:
                        dim_W = extract_dim(val)
                        if dim_W is not None: break
            if dim_L is None:
                for k, val in witness.items():
                    if isinstance(k, str) and 'L' in k:
                        dim_L = extract_dim(val)
                        if dim_L is not None: break
                        
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            v, w = witness
            dim_V = extract_dim(v)
            dim_W = extract_dim(w)
            
            str_v = str(v)
            str_w = str(w)
            if dim_V is None and dim_W is None:
                if ('Complexes' in str_v or 'CC' in str_v) and ('Reals' in str_w or 'RR' in str_w):
                    dim_V, dim_W, dim_L = 1, 1, 2
                elif ('Reals' in str_v or 'RR' in str_v) and ('Complexes' in str_w or 'CC' in str_w):
                    dim_V, dim_W, dim_L = 1, 1, 2
                    
        else:
            dim_V = extract_dim(getattr(witness, 'dim_V', None))
            if dim_V is None: 
                dim_V = extract_dim(getattr(witness, 'V', None))
            
            dim_W = extract_dim(getattr(witness, 'dim_W', None))
            if dim_W is None: 
                dim_W = extract_dim(getattr(witness, 'W', None))
            
            dim_L = extract_dim(getattr(witness, 'dim_L', None))
            if dim_L is None: 
                dim_L = extract_dim(getattr(witness, 'L', None))

        if dim_V is not None:
            h1 = dim_V >= 0
        if dim_W is not None:
            h2 = dim_W >= 0
        if dim_L is not None and dim_V is not None and dim_W is not None:
            neg_q = dim_L != dim_V * dim_W
            
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]