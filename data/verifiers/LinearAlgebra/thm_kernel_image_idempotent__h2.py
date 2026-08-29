import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness operator P, checks if it satisfies the hypotheses and falsifies the conclusion.
    The conjecture claims that for any idempotent operator P, ker(P) = im(I - P).
    This is true for linear operators, but false for general idempotent functions.
    """
    try:
        dim = None
        v = None
        P_v = None
        apply_P = None
        
        # Attempt to parse the witness as a callable function
        if callable(witness):
            for d in range(1, 6):
                v_mat = sp.Matrix([sp.Symbol(f'x{i}') for i in range(d)])
                v_tup = tuple(sp.Symbol(f'x{i}') for i in range(d))
                v_list = list(v_tup)
                
                # Try passing a sympy Matrix
                try:
                    res = witness(v_mat)
                    if isinstance(res, sp.Matrix) and res.shape == (d, 1):
                        dim = d
                        v = v_mat
                        P_v = res
                        def apply_P(vec, w=witness): return w(vec)
                        break
                    elif d == 1 and not isinstance(res, (sp.Matrix, tuple, list)):
                        dim = 1
                        v = v_mat
                        P_v = sp.Matrix([res])
                        def apply_P(vec, w=witness): return sp.Matrix([w(vec)])
                        break
                except Exception:
                    pass
                
                # Try passing unpacked arguments
                try:
                    res = witness(*v_tup)
                    if isinstance(res, (tuple, list)) and len(res) == d:
                        dim = d
                        v = sp.Matrix(v_tup)
                        P_v = sp.Matrix(res)
                        def apply_P(vec, w=witness): return sp.Matrix(w(*tuple(vec)))
                        break
                    elif d == 1 and not isinstance(res, (sp.Matrix, tuple, list)):
                        dim = 1
                        v = sp.Matrix(v_tup)
                        P_v = sp.Matrix([res])
                        def apply_P(vec, w=witness): return sp.Matrix([w(vec[0])])
                        break
                except Exception:
                    pass
                    
                # Try passing a tuple
                try:
                    res = witness(v_tup)
                    if isinstance(res, (tuple, list)) and len(res) == d:
                        dim = d
                        v = sp.Matrix(v_tup)
                        P_v = sp.Matrix(res)
                        def apply_P(vec, w=witness): return sp.Matrix(w(tuple(vec)))
                        break
                except Exception:
                    pass

                # Try passing a list
                try:
                    res = witness(v_list)
                    if isinstance(res, (tuple, list)) and len(res) == d:
                        dim = d
                        v = sp.Matrix(v_tup)
                        P_v = sp.Matrix(res)
                        def apply_P(vec, w=witness): return sp.Matrix(w(list(vec)))
                        break
                except Exception:
                    pass

        # Attempt to parse the witness as a tuple of (variables, expressions)
        elif isinstance(witness, tuple) and len(witness) == 2:
            vars_sym, exprs = witness
            if isinstance(vars_sym, (list, tuple)) and isinstance(exprs, (list, tuple)) and len(vars_sym) == len(exprs):
                dim = len(vars_sym)
                v = sp.Matrix(vars_sym)
                P_v = sp.Matrix(exprs)
                def apply_P(vec, vs=vars_sym, es=P_v):
                    subs_dict = {vs[i]: vec[i] for i in range(dim)}
                    return es.subs(subs_dict)
                    
        # Attempt to parse the witness as a sympy Matrix (linear operator)
        elif hasattr(witness, 'is_square') and witness.is_square:
            dim = witness.shape[0]
            v = sp.Matrix([sp.Symbol(f'x{i}') for i in range(dim)])
            P_v = witness * v
            def apply_P(vec, mat=witness):
                return mat * vec
                
        # Attempt to parse the witness as an explicit dictionary mapping
        elif isinstance(witness, dict):
            keys = list(witness.keys())
            if all(isinstance(k, tuple) for k in keys):
                dim = len(keys[0])
                h2 = True
                for val in witness.values():
                    if val not in witness or witness[val] != val:
                        h2 = False
                        break
                
                zero = tuple([0] * dim)
                neg_q = False
                for k in keys:
                    P_k = witness[k]
                    try:
                        diff = tuple(k[i] - P_k[i] for i in range(dim))
                        if diff in witness and witness[diff] != zero:
                            neg_q = True
                            break
                    except Exception:
                        pass
                return [True, h2, True, neg_q]

        if dim is None or apply_P is None:
            return [False, False, False, False]
            
        # Evaluate P(P(v)) and P(v - P(v))
        P_P_v = apply_P(P_v)
        I_minus_P_v = v - P_v
        P_I_minus_P_v = apply_P(I_minus_P_v)
        
        def is_zero_vec(vec):
            for i in range(dim):
                val = vec[i]
                if val == 0:
                    continue
                try:
                    if sp.simplify(val) == 0:
                        continue
                    if sp.expand(val) == 0:
                        continue
                except Exception:
                    pass
                return False
            return True
            
        # H_2: P is idempotent (P^2 = P)
        diff1 = P_P_v - P_v
        h2 = is_zero_vec(diff1)
        
        # ¬Q: ker(P) != im(I - P)
        # Since ker(P) is always a subset of im(I - P) for any function P,
        # ker(P) != im(I - P) is equivalent to im(I - P) not being a subset of ker(P).
        # This means there exists some v such that P(v - P(v)) != 0.
        diff2 = P_I_minus_P_v
        neg_q = not is_zero_vec(diff2)
        
        # H_1 and H_3 are structurally satisfied by the valid parsing of the operator
        return [True, h2, True, neg_q]
        
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: P is idempotent (P^2 = P)",
    "H_3: I is the identity operator on V",
    "¬Q: ker(P) != im(I - P)"
]

N_HYP = 3
NEG_Q_INDEX = 3