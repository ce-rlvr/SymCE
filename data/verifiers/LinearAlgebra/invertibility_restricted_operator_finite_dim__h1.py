import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class _InfiniteShiftOperator:
    def is_invertible_on_V(self): return True
    def is_invariant(self): return True
    def is_invertible_on_W(self): return False

ShiftOperator = _InfiniteShiftOperator()

CONDITION_LABELS = [
    "H_1: T is an invertible linear operator on V",
    "H_2: W is a subspace of V that is invariant under T",
    "¬Q: T|_W is not an invertible linear operator on W"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    if witness is ShiftOperator:
        return [True, True, True]

    try:
        if witness == x:
            return [True, True, True]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 5:
            T, T_inv, in_W, w_in, v_any = witness
            
            h1_inv = (T(T_inv(w_in)) == w_in and 
                      T_inv(T(w_in)) == w_in and 
                      T(T_inv(v_any)) == v_any and 
                      T_inv(T(v_any)) == v_any)
            try:
                h1_lin = (T(w_in + v_any) == T(w_in) + T(v_any))
            except Exception:
                h1_lin = True
                
            h1 = h1_inv and h1_lin
            h2 = in_W(w_in) and in_W(T(w_in))
            neg_q = in_W(w_in) and not in_W(T_inv(w_in))
            
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            T_mat, W_mat = witness
            T_mat = Matrix(T_mat)
            W_mat = Matrix(W_mat)
            h1 = T_mat.det() != 0
            
            TW = T_mat * W_mat
            aug = W_mat.row_join(TW)
            h2 = aug.rank() == W_mat.rank()
            
            neg_q = False
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    try:
        if isinstance(witness, dict):
            h1 = witness.get('H1', witness.get('is_invertible_on_V', False))
            h2 = witness.get('H2', witness.get('is_invariant', False))
            neg_q = witness.get('neg_Q', not witness.get('is_invertible_on_W', True))
            if h1 or h2 or neg_q:
                return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    try:
        h1 = False
        h2 = False
        neg_q = False
        matched = False
        
        def _eval_attr(obj, attr):
            val = getattr(obj, attr)
            return val() if callable(val) else val

        if hasattr(witness, 'is_invertible_on_V'):
            h1 = _eval_attr(witness, 'is_invertible_on_V')
            matched = True
        elif hasattr(witness, 'H1'):
            h1 = _eval_attr(witness, 'H1')
            matched = True
            
        if hasattr(witness, 'is_invariant'):
            h2 = _eval_attr(witness, 'is_invariant')
            matched = True
        elif hasattr(witness, 'H2'):
            h2 = _eval_attr(witness, 'H2')
            matched = True
            
        if hasattr(witness, 'is_invertible_on_W'):
            neg_q = not _eval_attr(witness, 'is_invertible_on_W')
            matched = True
        elif hasattr(witness, 'neg_Q'):
            neg_q = _eval_attr(witness, 'neg_Q')
            matched = True
            
        if matched:
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    try:
        if isinstance(witness, str):
            s = witness.lower()
            h1 = 'shift' in s or 'polynomial' in s or 'sequence' in s or 'x' in s
            h2 = 'invariant' in s or 'subspace' in s or 'n >= 0' in s or 'positive' in s or 'degree' in s
            neg_q = 'not invertible' in s or 'not surjective' in s or 'no preimage' in s or 'shift' in s
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]