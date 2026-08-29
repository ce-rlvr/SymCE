import sympy
import math
import itertools
import functools

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        # The witness is expected to be a dictionary containing the matrix A, 
        # the function f, and the variables vars.
        if isinstance(witness, dict):
            A = witness.get('A')
            f = witness.get('f')
            vars = witness.get('vars')
        elif isinstance(witness, tuple) and len(witness) == 3:
            A, f, vars = witness
        else:
            return [False, False]

        if not isinstance(vars, (list, tuple)):
            vars = [vars]

        # H_1: A is an n x n real positive definite matrix
        h1_ok = False
        if hasattr(A, 'is_square') and A.is_square:
            if all(A[i, j].is_real for i in range(A.rows) for j in range(A.cols)):
                # A matrix is positive definite if its symmetric part is positive definite
                A_sym = (A + A.T) / 2
                if A_sym.is_positive_definite == True:
                    h1_ok = True

        # neg_Q: The function f is not strictly convex on R^n
        neg_q_ok = False
        if f is not None and vars is not None:
            if len(vars) == 0:
                # A constant function is not strictly convex
                neg_q_ok = True
            else:
                # Try checking the Hessian first
                try:
                    H = sympy.hessian(f, vars)
                    if not H.free_symbols:
                        if H.is_positive_definite != True:
                            neg_q_ok = True
                except Exception:
                    pass

                if not neg_q_ok:
                    # Fallback to numerical check for non-strict convexity
                    pts = [
                        (0,) * len(vars),
                        (1,) * len(vars),
                        (-1,) * len(vars),
                        tuple([2 if i % 2 == 0 else -2 for i in range(len(vars))]),
                        tuple([-3 if i % 2 == 0 else 3 for i in range(len(vars))])
                    ]
                    for i in range(len(vars)):
                        pt = [0] * len(vars)
                        pt[i] = 1
                        pts.append(tuple(pt))
                        pt[i] = -1
                        pts.append(tuple(pt))
                        pt[i] = 2
                        pts.append(tuple(pt))
                        
                    pts = list(set(pts))
                    
                    for x, y in itertools.combinations(pts, 2):
                        mid = tuple((xi + yi) / 2.0 for xi, yi in zip(x, y))
                        val_x = float(f.subs(dict(zip(vars, x))))
                        val_y = float(f.subs(dict(zip(vars, y))))
                        val_mid = float(f.subs(dict(zip(vars, mid))))
                        
                        # If f(mid) >= 0.5*f(x) + 0.5*f(y), it is not strictly convex
                        if val_mid >= 0.5 * val_x + 0.5 * val_y - 1e-11:
                            neg_q_ok = True
                            break

        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: A is an n x n real positive definite matrix",
    "¬Q: The function f is not strictly convex on R^n"
]

N_HYP = 1
NEG_Q_INDEX = 1