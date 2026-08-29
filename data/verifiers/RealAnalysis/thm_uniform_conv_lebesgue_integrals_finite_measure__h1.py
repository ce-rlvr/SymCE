import sympy as sp
import math

# Top-level setup for the witness namespace
x = sp.Symbol('x', real=True)
n = sp.Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    witness is expected to be a tuple:
    (f_n, f, x_sym, n_sym, domain_limits, sup_bound)
    where:
      f_n: sympy Expr for f_n(x)
      f: sympy Expr for f(x)
      x_sym: sympy Symbol for the spatial variable
      n_sym: sympy Symbol for the sequence index
      domain_limits: tuple (a, b) for the integration domain (e.g., (0, sp.oo))
      sup_bound: sympy Expr in n bounding |f_n(x) - f(x)| from above on the domain
    """
    try:
        f_n, f, x_sym, n_sym, domain_limits, sup_bound = witness
    except Exception:
        return [False, False, False]

    # H_1: (f_n) is a sequence of measurable real-valued functions on X
    try:
        h1 = (isinstance(f_n, sp.Expr) and isinstance(f, sp.Expr) and 
              isinstance(domain_limits, (tuple, list)) and len(domain_limits) == 2)
        if h1:
            free_syms = f_n.free_symbols | f.free_symbols
            # Allow expressions to use x_sym, n_sym, and constants
            if not free_syms.issubset({x_sym, n_sym}):
                h1 = False
    except Exception:
        h1 = False

    # H_2: (f_n) converges uniformly to a function f on X
    try:
        lim_sup = sp.limit(sup_bound, n_sym, sp.oo)
        if sp.simplify(lim_sup) != 0:
            h2 = False
        else:
            h2 = True
            a, b = domain_limits
            # Numerically verify the supremum bound for a few values of n
            for n_val in [10, 50, 100]:
                bound_val = float(sup_bound.subs(n_sym, n_val))
                # Generate test points that might expose a failure of uniform convergence
                test_points = [0, 0.5, 1, 2, n_val/2, n_val, 2*n_val, n_val**2]
                x_vals = set()
                for tp in test_points:
                    for sign in [1, -1]:
                        val = sign * tp
                        try:
                            in_domain = True
                            if a != -sp.oo and val < float(a):
                                in_domain = False
                            if b != sp.oo and val > float(b):
                                in_domain = False
                            if in_domain:
                                x_vals.add(val)
                        except Exception:
                            pass
                
                for x_val in x_vals:
                    val_fn = f_n.subs({n_sym: n_val, x_sym: x_val}).evalf()
                    val_f = f.subs({n_sym: n_val, x_sym: x_val}).evalf()
                    if not val_fn.is_number or not val_f.is_number:
                        h2 = False
                        break
                    diff = abs(float(val_fn) - float(val_f))
                    if diff > bound_val + 1e-6:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: The sequence of Lebesgue integrals does not converge to the integral of f
    try:
        a, b = domain_limits
        
        # Compute integral of the limit function f
        int_f = sp.integrate(f, (x_sym, a, b))
        if int_f.has(sp.Integral):
            int_f_val = sp.Integral(f, (x_sym, a, b)).evalf()
        else:
            int_f_val = int_f.evalf()
            
        if not int_f_val.is_number:
            neg_q = False
        else:
            # Compute integral of the sequence f_n
            int_f_n = sp.integrate(f_n, (x_sym, a, b))
            
            is_symbolic_success = False
            if not int_f_n.has(sp.Integral):
                lim_int = sp.limit(int_f_n, n_sym, sp.oo)
                if not lim_int.has(sp.Limit):
                    is_symbolic_success = True
                    
            if is_symbolic_success:
                if sp.simplify(lim_int - int_f) != 0:
                    neg_q = True
                else:
                    neg_q = False
            else:
                # Fallback to numerical integration for a large n
                fn_val = f_n.subs(n_sym, 500)
                val = sp.Integral(fn_val, (x_sym, a, b)).evalf()
                
                if not val.is_number:
                    neg_q = False
                elif val == sp.oo or val == -sp.oo or val == sp.nan:
                    neg_q = True
                else:
                    if abs(float(val) - float(int_f_val)) > 1e-4:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of measurable real-valued functions on X",
    "H_2: (f_n) converges uniformly to a function f on X",
    "¬Q: The sequence of Lebesgue integrals does not converge to the integral of f"
]

N_HYP = 2
NEG_Q_INDEX = 2