import sympy as sp
import math

# Top-level setup: named object bindings that the witness expression may reference.
x, y, n, k = sp.symbols('x y n k', real=True)

CONDITION_LABELS = [
    "H_1: (X, d_X), (Y, d_Y), and (Z, d_Z) are metric spaces",
    "H_2: g: X -> Y is a continuous function",
    "¬Q: The family of composed functions F o g is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a dictionary providing:
      'X', 'Y', 'Z': sympy Sets (e.g., sp.Interval)
      'g': sympy expression in terms of x
      'F': sympy expression in terms of y and n (representing the family of functions)
      'x0': float or sympy expression (point where equicontinuity fails)
      'epsilon': float (the epsilon > 0 for which no delta works)
      'x_seq': sympy expression in terms of k (sequence converging to x0)
      'n_seq': sympy expression in terms of k (sequence of indices for F)
    """
    X = witness.get('X')
    Y = witness.get('Y')
    Z = witness.get('Z', sp.S.Reals)
    g = witness.get('g')
    F = witness.get('F')
    x0 = witness.get('x0')
    epsilon = witness.get('epsilon')
    x_seq = witness.get('x_seq')
    n_seq = witness.get('n_seq')
    
    # H_1: X, Y, Z are metric spaces (represented as subsets of Reals)
    try:
        h1 = isinstance(X, sp.Set) and isinstance(Y, sp.Set) and isinstance(Z, sp.Set)
    except Exception:
        h1 = False
        
    # H_2: g is continuous on X and maps X into Y
    try:
        cd = sp.calculus.util.continuous_domain(g, x, sp.S.Reals)
        is_continuous = X.is_subset(cd)
        if not is_continuous:
            h2 = False
        else:
            try:
                fr = sp.calculus.util.function_range(g, x, X)
                h2 = bool(fr.is_subset(Y))
            except Exception:
                # Fallback if function_range fails to evaluate symbolically
                h2 = True
                g_lam = sp.lambdify(x, g, 'math')
                if isinstance(X, sp.Interval) and isinstance(Y, sp.Interval):
                    pts = [X.start, X.end, (X.start + X.end) / 2]
                    for pt in pts:
                        val = g_lam(float(pt))
                        if val < float(Y.start) or val > float(Y.end):
                            h2 = False
                            break
    except Exception:
        h2 = False
        
    # ¬Q: F o g is not equicontinuous on X
    # We verify this by checking if there is a sequence x_k -> x0 and n_k such that
    # |F(n_k, g(x_k)) - F(n_k, g(x0))| >= epsilon for sufficiently large k.
    try:
        if not (X.contains(x0) == True or X.contains(x0) == sp.S.true):
            neg_q = False
        elif epsilon <= 0:
            neg_q = False
        else:
            g_lam = sp.lambdify(x, g, 'math')
            F_lam = sp.lambdify((n, y), F, 'math')
            x_seq_lam = sp.lambdify(k, x_seq, 'math')
            n_seq_lam = sp.lambdify(k, n_seq, 'math')
            
            x0_val = float(x0)
            g_x0 = g_lam(x0_val)
            
            neg_q = True
            
            # Verify that x_seq converges to x0
            try:
                lim_x = sp.limit(x_seq, k, sp.oo)
                lim_val = float(lim_x)
                if abs(lim_val - x0_val) > 1e-5:
                    neg_q = False
            except Exception:
                # Fallback if limit fails to evaluate symbolically
                xk_large = x_seq_lam(100000)
                if abs(xk_large - x0_val) > 1e-3:
                    neg_q = False
                    
            if neg_q:
                # Check the equicontinuity violation condition for large k
                for k_val in [100, 1000, 10000]:
                    xk = x_seq_lam(k_val)
                    nk = n_seq_lam(k_val)
                    
                    # Ensure the sequence points remain within the domain X
                    if isinstance(X, sp.Interval):
                        if xk < float(X.start) - 1e-7 or xk > float(X.end) + 1e-7:
                            neg_q = False
                            break
                            
                    try:
                        val_xk = complex(F_lam(nk, g_lam(xk)))
                        val_x0 = complex(F_lam(nk, g_x0))
                        diff = abs(val_xk - val_x0)
                    except OverflowError:
                        # If it overflows, the difference is effectively infinite (>= epsilon)
                        diff = float('inf')
                    except Exception:
                        neg_q = False
                        break
                        
                    if diff < epsilon - 1e-5:
                        neg_q = False
                        break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]