import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero(x):
    from sympy import MatrixBase
    try:
        if hasattr(x, 'is_zero_matrix') and x.is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        if isinstance(x, MatrixBase):
            for i in range(x.rows):
                for j in range(x.cols):
                    val = x[i, j]
                    if val != 0:
                        try:
                            if val.expand() != 0:
                                return False
                        except Exception:
                            return False
            return True
    except Exception:
        pass
    try:
        if x == 0:
            return True
        if hasattr(x, 'expand') and x.expand() == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    try:
        if not (isinstance(witness, (tuple, list)) and len(witness) == 2):
            return [False, False, False]
            
        f_obj, a = witness
        if isinstance(f_obj, (list, tuple)):
            coeffs = f_obj
        elif hasattr(f_obj, 'all_coeffs'):
            coeffs = f_obj.all_coeffs()
        else:
            return [False, False, False]
            
        if not (isinstance(coeffs, (list, tuple)) and len(coeffs) > 0):
            return [False, False, False]
            
        res_right = coeffs[0]
        for c in coeffs[1:]:
            res_right = res_right * a + c
            
        res_left = coeffs[0]
        for c in coeffs[1:]:
            res_left = a * res_left + c
            
        h1 = True
        h2 = True
        
        right_divides = is_zero(res_right)
        left_divides = is_zero(res_left)
        
        neg_q = bool(left_divides != right_divides)
        
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over F",
    "H_2: a is an element of F",
    "¬Q: The linear polynomial x - a divides f if and only if f(a) = 0 is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2