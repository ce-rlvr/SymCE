import sympy
from sympy import oo, Matrix, eye, zeros
from sympy.abc import x, y, z
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def normalize_inf(val):
    if isinstance(val, str):
        v = val.lower()
        if v in ["oo", "infinity", "inf", "infty"]:
            return oo
    if val == float('inf') or val == math.inf:
        return oo
    return val

def parse_bool(val):
    if isinstance(val, str):
        if val.lower() in ['false', 'f', '0', 'no']:
            return False
        if val.lower() in ['true', 't', '1', 'yes']:
            return True
    return bool(val)

def check_consistency(dim_W, rank_T, is_surj):
    """
    Ensures the provided witness is mathematically possible.
    A finite-dimensional space cannot be a counterexample.
    """
    try:
        if dim_W != oo:
            if is_surj and rank_T != dim_W:
                return False
            if not is_surj and bool(rank_T >= dim_W):
                return False
        else:
            if is_surj and rank_T != oo:
                return False
    except Exception:
        return False
    return True

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # 1. Witness is a SymPy Matrix (finite dimensional, cannot be a counterexample)
        if hasattr(witness, 'shape') and hasattr(witness, 'rank') and callable(witness.rank):
            h1 = True
            h2 = True
            dim_W = witness.shape[0]
            rank_T = witness.rank()
            is_surj = (rank_T == dim_W)
            if check_consistency(dim_W, rank_T, is_surj):
                equiv = (is_surj == (rank_T == dim_W))
                neg_q = not equiv

        # 2. Witness is a dictionary describing the properties
        elif isinstance(witness, dict):
            h1 = parse_bool(witness.get('is_vector_spaces', True))
            h2 = parse_bool(witness.get('is_linear_transformation', True))
            
            dim_W = None
            for k in ['dim_W', 'dim_codomain', 'dimW', 'W_dim']:
                if k in witness:
                    dim_W = normalize_inf(witness[k])
                    break
                    
            rank_T = None
            for k in ['rank_T', 'rank', 'rankT', 'T_rank']:
                if k in witness:
                    rank_T = normalize_inf(witness[k])
                    break
                    
            is_surj = None
            for k in ['is_surjective', 'surjective', 'surj']:
                if k in witness:
                    is_surj = witness[k]
                    break
                    
            if dim_W is not None and rank_T is not None and is_surj is not None:
                is_surj = parse_bool(is_surj)
                if check_consistency(dim_W, rank_T, is_surj):
                    equiv = (is_surj == (rank_T == dim_W))
                    neg_q = not equiv

        # 3. Witness is an object with attributes
        elif hasattr(witness, 'dim_W') or hasattr(witness, 'dim_codomain'):
            dim_W = getattr(witness, 'dim_W', getattr(witness, 'dim_codomain', None))
            rank_T = getattr(witness, 'rank_T', getattr(witness, 'rank', None))
            is_surj = getattr(witness, 'is_surjective', getattr(witness, 'surjective', None))
            
            dim_W = normalize_inf(dim_W)
            rank_T = normalize_inf(rank_T)
            
            if dim_W is not None and rank_T is not None and is_surj is not None:
                is_surj = parse_bool(is_surj)
                if check_consistency(dim_W, rank_T, is_surj):
                    h1 = parse_bool(getattr(witness, 'is_vector_spaces', True))
                    h2 = parse_bool(getattr(witness, 'is_linear_transformation', True))
                    equiv = (is_surj == (rank_T == dim_W))
                    neg_q = not equiv

        # 4. Witness is a tuple: (dim_W, rank_T, is_surjective)
        elif isinstance(witness, tuple) and len(witness) >= 3:
            dim_W = normalize_inf(witness[0])
            rank_T = normalize_inf(witness[1])
            is_surj = parse_bool(witness[2])
            if check_consistency(dim_W, rank_T, is_surj):
                h1 = True
                h2 = True
                equiv = (is_surj == (rank_T == dim_W))
                neg_q = not equiv

        # 5. Witness is a string describing a known counterexample
        elif isinstance(witness, str):
            h1 = True
            h2 = True
            s = witness.lower()
            if any(x in s for x in ["right shift", "right_shift", "integration", "integral", "multiplication by x", "times x", "shift operator"]):
                neg_q = True
            else:
                neg_q = False
                
        # 6. Witness is a function representing a known counterexample
        elif callable(witness):
            name = getattr(witness, '__name__', '').lower()
            if any(x in name for x in ["shift", "integral", "mul_x"]):
                h1 = True
                h2 = True
                neg_q = True

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: T: V -> W is a linear transformation",
    "¬Q: T is surjective if and only if rank(T) = dim(W) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2