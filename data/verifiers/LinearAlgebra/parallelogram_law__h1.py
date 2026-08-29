import sympy
from sympy import Matrix, eye, zeros, oo, simplify
import sympy.abc
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Witness can be (u, v) defaulting to L1 norm, or (u, v, p) for Lp norm
        if isinstance(witness, tuple) and len(witness) == 3:
            u, v, p = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            u, v = witness
            p = 1
        else:
            return [False, False]
            
        if p in ('inf', 'oo', oo):
            p = oo
            
        # H_1: Let u and v be vectors in V.
        try:
            if not isinstance(u, (list, tuple, Matrix)):
                u_val = [u]
            else:
                u_val = u
            if not isinstance(v, (list, tuple, Matrix)):
                v_val = [v]
            else:
                v_val = v
                
            u_mat = Matrix(u_val)
            v_mat = Matrix(v_val)
            
            h1 = (u_mat.shape == v_mat.shape) and (len(u_mat) > 0)
        except Exception:
            h1 = False
            
        # ¬Q: ||u + v||^2 + ||u - v||^2 != 2||u||^2 + 2||v||^2
        try:
            if not h1:
                neg_q = False
            else:
                norm_u = u_mat.norm(p)
                norm_v = v_mat.norm(p)
                norm_u_plus_v = (u_mat + v_mat).norm(p)
                norm_u_minus_v = (u_mat - v_mat).norm(p)
                
                left = norm_u_plus_v**2 + norm_u_minus_v**2
                right = 2 * norm_u**2 + 2 * norm_v**2
                
                diff = simplify(left - right)
                try:
                    if diff.is_number:
                        neg_q = bool(abs(complex(diff)) > 1e-12)
                    else:
                        neg_q = bool(diff != 0)
                except Exception:
                    neg_q = bool(diff != 0)
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: u and v are vectors in V",
    "¬Q: ||u + v||^2 + ||u - v||^2 != 2||u||^2 + 2||v||^2"
]

N_HYP = 1
NEG_Q_INDEX = 1