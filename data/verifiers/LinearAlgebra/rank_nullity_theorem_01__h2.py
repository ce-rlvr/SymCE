import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_dim(witness, keys):
    for k in keys:
        if k in witness:
            return witness[k]
    return None

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false Rank-Nullity conjecture
    (where the hypothesis that T is a linear transformation is dropped).
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # 1. Witness as a dictionary of dimensions
        if isinstance(witness, dict):
            v_dim = get_dim(witness, ['dim(V)', 'V_dim', 'dim_V', 'v_dim', 'dim_v'])
            ker_dim = get_dim(witness, ['dim(ker(T))', 'ker_dim', 'dim_ker', 'nullity'])
            im_dim = get_dim(witness, ['dim(im(T))', 'im_dim', 'dim_im', 'rank'])
            
            if v_dim is not None and ker_dim is not None and im_dim is not None:
                h1 = witness.get('is_vs', witness.get('vector_spaces', True))
                h2 = float(v_dim) < float('inf')
                neg_q = v_dim != ker_dim + im_dim
                return [bool(h1), bool(h2), bool(neg_q)]

        # 2. Witness as an object with dimension attributes
        v_dim = None
        for k in ['dim_V', 'V_dim', 'dim_v', 'v_dim']:
            if hasattr(witness, k):
                v_dim = getattr(witness, k)
                break
        
        ker_dim = None
        for k in ['dim_ker', 'ker_dim', 'nullity']:
            if hasattr(witness, k):
                ker_dim = getattr(witness, k)
                break
                
        im_dim = None
        for k in ['dim_im', 'im_dim', 'rank']:
            if hasattr(witness, k):
                im_dim = getattr(witness, k)
                break
                
        if v_dim is not None and ker_dim is not None and im_dim is not None:
            h1 = getattr(witness, 'is_vs', getattr(witness, 'vector_spaces', True))
            h2 = float(v_dim) < float('inf')
            neg_q = v_dim != ker_dim + im_dim
            return [bool(h1), bool(h2), bool(neg_q)]

        # 3. Witness as a tuple: (dim_V, dim_ker, dim_im)
        if isinstance(witness, tuple) and len(witness) >= 3:
            try:
                v_dim_float = float(witness[0])
                ker_dim_float = float(witness[1])
                im_dim_float = float(witness[2])
                h1 = True
                h2 = v_dim_float < float('inf')
                neg_q = witness[0] != witness[1] + witness[2]
                return [bool(h1), bool(h2), bool(neg_q)]
            except (ValueError, TypeError):
                pass

        # 4. Witness as a SymPy Matrix (will fail neg_q since Rank-Nullity holds for matrices, but included for completeness)
        if hasattr(witness, 'cols') and hasattr(witness, 'nullspace'):
            v_dim = witness.cols
            ker_dim = len(witness.nullspace())
            im_dim = len(witness.columnspace())
            h1 = True
            h2 = True
            neg_q = v_dim != ker_dim + im_dim
            return [bool(h1), bool(h2), bool(neg_q)]

    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: V is finite-dimensional",
    "¬Q: dim(V) != dim(ker(T)) + dim(im(T))"
]

N_HYP = 2
NEG_Q_INDEX = 2