import sympy
from sympy import eye, zeros
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "¬Q: V/ker(T) is not isomorphic to the image of T"
]
N_HYP = 1
NEG_Q_INDEX = 1

def evaluate_T(T, v, F):
    try:
        if isinstance(T, dict):
            res = T[v]
        elif isinstance(T, sympy.Matrix):
            res = T * sympy.Matrix(v)
        elif isinstance(T, sympy.Lambda):
            if len(T.variables) == 1:
                res = T(v[0]) if len(v) == 1 else T(v)
            else:
                res = T(*v)
        else:
            try:
                if len(v) == 1:
                    res = T(v[0])
                else:
                    res = T(*v)
            except TypeError:
                res = T(v)
            
        if isinstance(res, sympy.Matrix):
            return tuple(int(x) % F for x in res)
        elif isinstance(res, (tuple, list, sympy.Tuple)):
            return tuple(int(x) % F for x in res)
        else:
            return (int(res) % F,)
    except Exception:
        return None

def extract_witness(witness):
    V_dim = None
    W_dim = None
    F_val = None
    T = None
    
    if isinstance(witness, dict) and 'T' in witness:
        V_dim = witness.get('V_dim')
        W_dim = witness.get('W_dim')
        F_val = witness.get('F')
        T = witness.get('T')
    elif isinstance(witness, (tuple, list)) and len(witness) == 3:
        V_dim, W_dim, T = witness
    else:
        T = witness

    if isinstance(T, sympy.Matrix):
        W_dim, V_dim = T.shape
    elif isinstance(T, dict) and len(T) > 0:
        sample_k = next(iter(T.keys()))
        sample_v = T[sample_k]
        if V_dim is None:
            V_dim = len(sample_k) if isinstance(sample_k, (tuple, list)) else 1
        if W_dim is None:
            W_dim = len(sample_v) if isinstance(sample_v, (tuple, list)) else 1

    if V_dim is None or W_dim is None:
        if isinstance(T, sympy.Lambda):
            V_dim = len(T.variables)
            try:
                zero_val = T(*[0]*V_dim)
                if isinstance(zero_val, (tuple, list, sympy.Tuple, sympy.Matrix)):
                    W_dim = len(zero_val)
                else:
                    W_dim = 1
            except Exception:
                W_dim = 1
        elif callable(T) and not isinstance(T, type):
            try:
                if hasattr(T, '__code__'):
                    V_dim = T.__code__.co_argcount
                else:
                    V_dim = 1
                
                if V_dim == 1:
                    try:
                        zero_val = T(0)
                    except Exception:
                        zero_val = T((0, 0))
                        V_dim = 2
                else:
                    zero_val = T(*[0]*V_dim)
                    
                if isinstance(zero_val, (tuple, list, sympy.Tuple, sympy.Matrix)):
                    W_dim = len(zero_val)
                else:
                    W_dim = 1
            except Exception:
                V_dim = 2
                W_dim = 2
        else:
            V_dim = 2
            W_dim = 2

    return V_dim, W_dim, F_val, T

def check_witness_over_F(V_dim, W_dim, T, F):
    if F**V_dim > 10000:
        return None
        
    elements = list(range(F))
    V_vectors = list(itertools.product(elements, repeat=V_dim))
    
    T_map = {}
    for v in V_vectors:
        res = evaluate_T(T, v, F)
        if res is None:
            return None
        if len(res) != W_dim:
            res = tuple(list(res) + [0]*(W_dim - len(res)))[:W_dim]
        T_map[v] = res
        
    zero_W = tuple([0]*W_dim)
    ker_T = set(v for v in V_vectors if T_map[v] == zero_W)
    Im_T = set(T_map.values())
    
    zero_V = tuple([0]*V_dim)
    if zero_V not in ker_T:
        ker_is_subspace = False
    else:
        ker_is_subspace = True
        for v1 in ker_T:
            for v2 in ker_T:
                if tuple((x + y) % F for x, y in zip(v1, v2)) not in ker_T:
                    ker_is_subspace = False
                    break
            if not ker_is_subspace: break
            for c in range(F):
                if tuple((c * x) % F for x in v1) not in ker_T:
                    ker_is_subspace = False
                    break
            if not ker_is_subspace: break

    if zero_W not in Im_T:
        im_is_subspace = False
    else:
        im_is_subspace = True
        for w1 in Im_T:
            for w2 in Im_T:
                if tuple((x + y) % F for x, y in zip(w1, w2)) not in Im_T:
                    im_is_subspace = False
                    break
            if not im_is_subspace: break
            for c in range(F):
                if tuple((c * x) % F for x in w1) not in Im_T:
                    im_is_subspace = False
                    break
            if not im_is_subspace: break

    if not ker_is_subspace or not im_is_subspace:
        return True
        
    if len(V_vectors) % len(ker_T) != 0:
        return True
    size_V_mod_ker = len(V_vectors) // len(ker_T)
    size_Im = len(Im_T)
    
    return size_V_mod_ker != size_Im

def conditions(witness):
    try:
        V_dim, W_dim, F_val, T = extract_witness(witness)
        h1 = isinstance(V_dim, int) and V_dim > 0 and isinstance(W_dim, int) and W_dim > 0
    except Exception:
        h1 = False

    neg_q = False
    try:
        if h1 and T is not None:
            fields_to_check = [F_val] if F_val is not None and isinstance(F_val, int) else [2, 3, 5, 7, 11]
            for F in fields_to_check:
                res = check_witness_over_F(V_dim, W_dim, T, F)
                if res is True:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]