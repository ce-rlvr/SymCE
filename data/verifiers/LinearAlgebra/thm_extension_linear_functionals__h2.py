import itertools
import sympy
from sympy import Matrix, zeros, eye
from sympy.ntheory import isprime

# Top-level setup for standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subset_span(W_vecs, V_vecs):
    if not W_vecs:
        return True
    if not V_vecs:
        return all(all(x == 0 for x in w) for w in W_vecs)
    
    V_mat = Matrix.hstack(*V_vecs)
    rank_V = V_mat.rank()
    for w in W_vecs:
        if w.shape[0] != V_mat.shape[0]:
            return False
        M_w = V_mat.row_join(w)
        if M_w.rank() > rank_V:
            return False
    return True

def is_valid_f_list(W_vecs, f_list):
    if len(W_vecs) != len(f_list):
        return False
    if not W_vecs:
        return True
    W_mat = Matrix.hstack(*W_vecs)
    f_mat = Matrix([f_list])
    M = W_mat.T
    M_f = M.row_join(f_mat.T)
    return M.rank() == M_f.rank()

def conditions_format_B(witness):
    try:
        p = witness['p']
        V = witness['V']
        V_add = witness['V_add']
        V_mul = witness['V_mul']
        W = witness['W']
        W_add = witness['W_add']
        W_mul = witness['W_mul']
        f = witness['f']
    except Exception:
        return [False, False, False]
        
    def get_val(func_or_dict, *args):
        if isinstance(func_or_dict, dict):
            return func_or_dict[args]
        else:
            return func_or_dict(*args)
            
    def is_vs(S, S_add, S_mul):
        if not S: return False
        if not isprime(p): return False
        for u in S:
            for v in S:
                if get_val(S_add, u, v) not in S: return False
        for c in range(p):
            for v in S:
                if get_val(S_mul, c, v) not in S: return False
        for u in S:
            for v in S:
                for w in S:
                    if get_val(S_add, get_val(S_add, u, v), w) != get_val(S_add, u, get_val(S_add, v, w)): return False
        for u in S:
            for v in S:
                if get_val(S_add, u, v) != get_val(S_add, v, u): return False
        zero = None
        for z in S:
            if all(get_val(S_add, z, v) == v for v in S):
                zero = z
                break
        if zero is None: return False
        for v in S:
            if not any(get_val(S_add, v, u) == zero for u in S): return False
        for v in S:
            if get_val(S_mul, 1, v) != v: return False
        for c in range(p):
            for d in range(p):
                for v in S:
                    if get_val(S_mul, c, get_val(S_mul, d, v)) != get_val(S_mul, (c*d)%p, v): return False
        for c in range(p):
            for u in S:
                for v in S:
                    if get_val(S_mul, c, get_val(S_add, u, v)) != get_val(S_add, get_val(S_mul, c, u), get_val(S_mul, c, v)): return False
        for c in range(p):
            for d in range(p):
                for v in S:
                    if get_val(S_mul, (c+d)%p, v) != get_val(S_add, get_val(S_mul, c, v), get_val(S_mul, d, v)): return False
        return True

    try:
        h1 = is_vs(V, V_add, V_mul)
    except Exception:
        h1 = False
        
    try:
        h2 = is_vs(W, W_add, W_mul)
        if h2:
            for u in W:
                for v in W:
                    if get_val(f, get_val(W_add, u, v)) != (get_val(f, u) + get_val(f, v)) % p:
                        h2 = False
            for c in range(p):
                for v in W:
                    if get_val(f, get_val(W_mul, c, v)) != (c * get_val(f, v)) % p:
                        h2 = False
    except Exception:
        h2 = False
        
    try:
        if not all(w in V for w in W):
            neg_q = True
        else:
            V_list = list(V)
            n = len(V_list)
            if p**n > 100000:
                neg_q = False
            else:
                exists = False
                for vals in itertools.product(range(p), repeat=n):
                    f_dict = dict(zip(V_list, vals))
                    valid = True
                    for u in V_list:
                        for v in V_list:
                            if f_dict[get_val(V_add, u, v)] != (f_dict[u] + f_dict[v]) % p:
                                valid = False; break
                        if not valid: break
                    if not valid: continue
                    for c in range(p):
                        for v in V_list:
                            if f_dict[get_val(V_mul, c, v)] != (c * f_dict[v]) % p:
                                valid = False; break
                        if not valid: break
                    if not valid: continue
                    
                    match = True
                    for w in W:
                        if f_dict[w] != get_val(f, w):
                            match = False; break
                    if match:
                        exists = True; break
                neg_q = not exists
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

def conditions(witness):
    if isinstance(witness, dict) and 'p' in witness and 'V_add' in witness:
        return conditions_format_B(witness)
        
    try:
        if isinstance(witness, dict):
            V = witness.get('V')
            W = witness.get('W')
            f = witness.get('f')
        else:
            V, W, f = witness
    except Exception:
        return [False, False, False]
        
    if isinstance(V, int) and isinstance(W, int):
        try:
            h1 = V >= 0
            h2 = False
            if W >= 0:
                if isinstance(f, Matrix) and (f.shape == (1, W) or f.shape == (W, 1)):
                    h2 = True
                elif callable(f):
                    h2 = True
                elif isinstance(f, list) and len(f) == W:
                    h2 = True
            neg_q = (V != W)
            return [h1, h2, neg_q]
        except Exception:
            return [False, False, False]
            
    try:
        h1 = False
        if isinstance(V, list) and all(isinstance(v, Matrix) for v in V):
            h1 = True
        elif isinstance(V, Matrix):
            V = [V.col(i) for i in range(V.cols)]
            h1 = True
    except Exception:
        h1 = False
        
    try:
        h2 = False
        if isinstance(W, list) and all(isinstance(w, Matrix) for w in W):
            pass
        elif isinstance(W, Matrix):
            W = [W.col(i) for i in range(W.cols)]
        else:
            raise ValueError
            
        if isinstance(f, Matrix):
            if f.rows == 1:
                if not W or f.cols == W[0].rows:
                    h2 = True
            elif f.cols == 1:
                if not W or f.rows == W[0].rows:
                    h2 = True
        elif callable(f):
            w1 = W[0] if W else None
            w2 = W[1] if len(W) > 1 else w1
            if w1 is not None:
                if f(w1 + w2) == f(w1) + f(w2) and f(2 * w1) == 2 * f(w1):
                    h2 = True
            else:
                h2 = True
        elif isinstance(f, list):
            if is_valid_f_list(W, f):
                h2 = True
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_subset_span(W, V)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: f is a linear functional on W",
    "¬Q: There does not exist a linear functional F on V such that F(w) = f(w) for all w in W"
]

N_HYP = 2
NEG_Q_INDEX = 2