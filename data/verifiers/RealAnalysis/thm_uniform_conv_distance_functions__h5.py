import sympy
import sympy.abc
import math
import itertools
import functools

# Top-level setup for Real Analysis domain
x, y, z, n = sympy.symbols('x y z n', real=True)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample to the conjecture.
    Returns a list of booleans: [H_1, H_2, H_3, H_4, neg_Q].
    """
    # 1. Try to evaluate the witness as a finite metric space model
    try:
        X = witness.X
        d = witness.d
        A_n = witness.A_n
        A = witness.A
        f_n = witness.f_n
        f = witness.f
        
        # H1: (X, d) is a metric space
        h1 = True
        for pt_x in X:
            for pt_y in X:
                if d(pt_x, pt_y) < 0: h1 = False
                if d(pt_x, pt_y) != d(pt_y, pt_x): h1 = False
                if (d(pt_x, pt_y) == 0) != (pt_x == pt_y): h1 = False
                for pt_z in X:
                    if d(pt_x, pt_z) > d(pt_x, pt_y) + d(pt_y, pt_z) + 1e-9: h1 = False
                    
        # H2: (A_n) is a sequence of non-empty compact subsets of X
        h2 = True
        for i in range(1, 6):
            An = A_n(i)
            if not An: h2 = False
            for a in An:
                if a not in X: h2 = False
                
        # H3: (A_n) converges to a non-empty compact subset A in the Hausdorff metric
        h3 = True
        if not A: h3 = False
        for a in A:
            if a not in X: h3 = False
            
        def d_H(U, V):
            if not U or not V: return float('inf')
            sup_U = max(min(d(u, v) for v in V) for u in U)
            sup_V = max(min(d(u, v) for u in U) for v in V)
            return max(sup_U, sup_V)
        
        d_H_vals = [d_H(A_n(i), A) for i in range(1, 20)]
        if d_H_vals[-1] > 1e-5: h3 = False
        
        # H4: f_n(x) = inf_{a \in A_n} d(x, a)
        h4 = True
        for i in range(1, 6):
            for pt_x in X:
                expected = min(d(pt_x, a) for a in A_n(i))
                if abs(f_n(i, pt_x) - expected) > 1e-9: h4 = False
                
        # neg_Q: The sequence of functions (f_n) does NOT converge uniformly to f on X
        converges = True
        for pt_x in X:
            limit_correct = True
            for i in range(15, 20):
                if abs(f_n(i, pt_x) - f(pt_x)) > 1e-5:
                    limit_correct = False
            if not limit_correct:
                converges = False
                break
        neg_q = not converges
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # 2. Fallback to dictionary or object attributes/methods
    def get_bool(obj, keys):
        for k in keys:
            try:
                if isinstance(obj, dict) and k in obj:
                    val = obj[k]
                elif hasattr(obj, k):
                    val = getattr(obj, k)
                else:
                    continue
                if callable(val):
                    return bool(val())
                return bool(val)
            except Exception:
                pass
        return False

    h1 = get_bool(witness, ['h1', 'is_metric_space'])
    h2 = get_bool(witness, ['h2', 'are_compact', 'is_compact'])
    h3 = get_bool(witness, ['h3', 'converges_in_hausdorff'])
    h4 = get_bool(witness, ['h4', 'is_inf_distance'])
    
    neg_q = False
    try:
        if isinstance(witness, dict) and 'converges_uniformly' in witness:
            val = witness['converges_uniformly']
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'converges_uniformly'):
            val = getattr(witness, 'converges_uniformly')
            neg_q = not bool(val() if callable(val) else val)
        else:
            neg_q = get_bool(witness, ['neg_q'])
    except Exception:
        pass

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: (A_n) is a sequence of non-empty compact subsets of X",
    "H_3: (A_n) converges to a non-empty compact subset A in the Hausdorff metric",
    "H_4: f_n(x) = inf_{a in A_n} d(x, a)",
    "¬Q: The sequence of functions (f_n) does not converge uniformly to f on X"
]

N_HYP = 4
NEG_Q_INDEX = 4