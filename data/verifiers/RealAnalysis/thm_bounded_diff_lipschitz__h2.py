import sympy
import math
import itertools

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys:
      'f': sympy expression or list of sympy expressions
      'vars': list of sympy symbols (or a single symbol)
      'U': sympy Set (e.g., Interval or ProductSet)
      'M': non-negative real number
    """
    try:
        f = witness['f']
        vars = witness['vars']
        if not isinstance(vars, (list, tuple)):
            vars = [vars]
        U = witness['U']
        M = float(witness['M'])
    except Exception:
        return [False, False, False]
        
    # H_1: U is an open convex subset of R^n
    h1 = False
    try:
        if isinstance(U, sympy.Interval):
            h1 = U.is_open and U.is_real
        elif isinstance(U, sympy.ProductSet):
            h1 = all(isinstance(s, sympy.Interval) and s.is_open for s in U.sets)
        elif hasattr(U, 'is_open') and hasattr(U, 'is_convex'):
            h1 = U.is_open and U.is_convex
    except Exception:
        pass

    # H_2: There exists M >= 0 such that ||Df(x)|| <= M for all x in U
    h2 = False
    points = []
    try:
        if M >= 0:
            if not isinstance(f, (list, tuple, sympy.Matrix)):
                f_mat = sympy.Matrix([f])
            else:
                f_mat = sympy.Matrix(f)
            
            J = f_mat.jacobian(vars)
            
            intervals = []
            if isinstance(U, sympy.Interval):
                intervals = [U]
            elif isinstance(U, sympy.ProductSet):
                intervals = U.sets
                
            if intervals:
                grid_1d = []
                for iv in intervals:
                    start = float(iv.start) if iv.start.is_finite else -10.0
                    end = float(iv.end) if iv.end.is_finite else 10.0
                    # Avoid exact boundaries to stay strictly inside the open set
                    start += 0.05 * (end - start)
                    end -= 0.05 * (end - start)
                    n_points = 5
                    step = (end - start) / (n_points - 1) if n_points > 1 else 0
                    grid_1d.append([start + i * step for i in range(n_points)])
                    
                points = list(itertools.product(*grid_1d))
                
                h2 = True
                for pt in points:
                    subs_dict = dict(zip(vars, pt))
                    J_val = J.subs(subs_dict).evalf()
                    norm = float(J_val.norm(2))
                    if norm > M + 1e-5:
                        h2 = False
                        break
    except Exception:
        pass

    # ¬Q: f is not Lipschitz continuous on U with Lipschitz constant M
    neg_q = False
    try:
        if points:
            f_vals = []
            for pt in points:
                subs_dict = dict(zip(vars, pt))
                f_vals.append(f_mat.subs(subs_dict).evalf())
                
            for i, j in itertools.combinations(range(len(points)), 2):
                p1 = points[i]
                p2 = points[j]
                v1 = f_vals[i]
                v2 = f_vals[j]
                
                dist_f = float((v1 - v2).norm(2))
                dist_x = math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))
                
                if dist_f > M * dist_x + 1e-5:
                    neg_q = True
                    break
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U is an open convex subset of R^n",
    "H_2: There exists M >= 0 such that ||Df(x)|| <= M for all x in U",
    "¬Q: f is not Lipschitz continuous on U with Lipschitz constant M"
]

N_HYP = 2
NEG_Q_INDEX = 2