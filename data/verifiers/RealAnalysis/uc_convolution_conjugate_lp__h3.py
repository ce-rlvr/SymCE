import sympy as sp
import math

# Top-level setup
x, y = sp.symbols('x y', real=True)

def is_finite_positive(val):
    """Helper to check if a SymPy value is a finite non-negative real number."""
    try:
        if val in (sp.oo, -sp.oo, sp.zoo, sp.nan):
            return False
        if hasattr(val, 'is_real') and not val.is_real:
            val = sp.re(val)
        fval = float(val)
        return fval >= 0 and fval < float('inf')
    except Exception:
        return False

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "If p, q > 1 with 1/p + 1/q = 1, and f in L^p(R^n), then f * g is uniformly continuous."
    (The hypothesis g in L^q was dropped).
    """
    try:
        p = witness.get('p')
        q = witness.get('q')
        n = witness.get('n', 1)
        f = witness.get('f')
        g = witness.get('g')
        x_sym = witness.get('x', x)
        x0 = witness.get('x0', 0)
    except Exception:
        return [False, False, False]
        
    # We only verify 1D counterexamples for simplicity, which is sufficient to disprove the general R^n case.
    if n != 1:
        return [False, False, False]
        
    # H_1: p and q are real numbers strictly greater than 1 such that 1/p + 1/q = 1
    try:
        p_val = float(p)
        q_val = float(q)
        h1 = (p_val > 1.0) and (q_val > 1.0) and math.isclose(1/p_val + 1/q_val, 1.0, rel_tol=1e-7)
    except Exception:
        h1 = False
        
    # H_2: f \in L^p(R^n)
    try:
        y_sym = sp.Symbol('y', real=True)
        f_y = f.subs(x_sym, y_sym)
        
        int_val = sp.integrate(sp.Abs(f_y)**p, (y_sym, -sp.oo, sp.oo))
        if isinstance(int_val, sp.Integral):
            int_val = int_val.evalf()
            
        h2 = is_finite_positive(int_val)
    except Exception:
        h2 = False
        
    # ¬Q: The convolution f * g is not uniformly continuous on R^n
    try:
        neg_q = False
        y_sym = sp.Symbol('y', real=True)
        f_y = f.subs(x_sym, y_sym)
        g_shifted = g.subs(x_sym, x0 - y_sym)
        
        # Mode 1: Check if the convolution diverges at a specific point x0 (meaning it's not a well-defined function)
        conv_x0 = sp.integrate(f_y * g_shifted, (y_sym, -sp.oo, sp.oo))
        
        if not isinstance(conv_x0, sp.Integral):
            if conv_x0 in (sp.oo, -sp.oo, sp.zoo, sp.nan):
                neg_q = True
            else:
                try:
                    fval = float(conv_x0)
                    if math.isinf(fval) or math.isnan(fval):
                        neg_q = True
                except Exception:
                    pass
        else:
            try:
                val = conv_x0.evalf()
                if val in (sp.oo, -sp.oo, sp.zoo, sp.nan):
                    neg_q = True
                else:
                    fval = float(val)
                    if math.isinf(fval) or math.isnan(fval):
                        neg_q = True
            except ValueError as e:
                if "divergent" in str(e).lower() or "not converge" in str(e).lower():
                    neg_q = True
            except Exception:
                pass
                
        # Mode 2: Check if the witness provides a sequence showing non-uniform continuity
        if not neg_q and 'x_k' in witness and 'y_k' in witness and 'k' in witness:
            k_sym = witness['k']
            x_k_expr = witness['x_k']
            y_k_expr = witness['y_k']
            
            k_val = 1000.0
            x_val = float(x_k_expr.subs(k_sym, k_val))
            y_val = float(y_k_expr.subs(k_sym, k_val))
            
            if abs(x_val - y_val) < 0.1:
                expr_x = f_y * g.subs(x_sym, x_val - y_sym)
                expr_y = f_y * g.subs(x_sym, y_val - y_sym)
                
                try:
                    conv_x = sp.Integral(expr_x, (y_sym, -sp.oo, sp.oo)).evalf()
                    conv_y = sp.Integral(expr_y, (y_sym, -sp.oo, sp.oo)).evalf()
                    
                    cx = float(conv_x)
                    cy = float(conv_y)
                    if abs(cx - cy) > 0.1:
                        neg_q = True
                except ValueError as e:
                    if "divergent" in str(e).lower() or "not converge" in str(e).lower():
                        neg_q = True
                except Exception:
                    pass
                    
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p and q are real numbers strictly greater than 1 such that 1/p + 1/q = 1",
    "H_2: f in L^p(R^n)",
    "¬Q: The convolution f * g is not uniformly continuous on R^n"
]

N_HYP = 2
NEG_Q_INDEX = 2