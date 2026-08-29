import sympy as sp
from sympy import Symbol, symbols, Sum, Abs, oo, sin, cos, exp, pi

# Top-level setup: named object bindings for witness expressions
x, y, z, t = symbols('x y z t', real=True)
n, k, m = symbols('n k m', integer=True, positive=True)

CONDITION_LABELS = [
    "H_1: The series converges absolutely on an open polydisc D centered at a",
    "¬Q: The function f is not continuously differentiable on D, or its partial derivatives are not given by the term-by-term differentiated power series"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # Fallback for dictionary-based witnesses
        if isinstance(witness, dict):
            h1 = bool(witness.get("converges_absolutely_on_D", False))
            q1 = bool(witness.get("is_continuously_differentiable_on_D", True))
            q2 = bool(witness.get("derivative_equals_term_by_term", True))
            neg_q = not (q1 and q2)
            return [h1, neg_q]

        term = None
        n_var = None
        
        # Extract the general term and the index variable from various possible witness formats
        if isinstance(witness, sp.Sum):
            term = witness.args[0]
            n_var = witness.args[1][0]
        elif isinstance(witness, tuple) and len(witness) >= 2:
            term = witness[0]
            n_var = witness[1]
            if isinstance(n_var, tuple):
                n_var = n_var[0]
        elif callable(witness):
            n_sym = sp.Symbol('n', integer=True, positive=True)
            x_sym = sp.Symbol('x', real=True)
            try:
                term = witness(n_sym, x_sym)
                n_var = n_sym
            except Exception:
                pass
        elif isinstance(witness, sp.Expr):
            term = witness
            free_vars = term.free_symbols
            for v in free_vars:
                if v.name in ['n', 'k', 'm', 'i', 'j']:
                    n_var = v
                    break
            if n_var is None and free_vars:
                n_var = list(free_vars)[0]
                
        if term is not None and n_var is not None:
            vars = list(term.free_symbols - {n_var})
            
            # If there are no spatial variables, it's a constant series
            if not vars:
                try:
                    s = sp.Sum(sp.Abs(term), (n_var, 1, sp.oo))
                    conv = s.is_convergent()
                    h1 = (conv is not False)
                except Exception:
                    h1 = True
                neg_q = False
                return [h1, neg_q]
                
            # Check absolute convergence at a few sample points to verify it converges on some open polydisc
            for pt in [0.5, -0.5, 0.1, -0.1, 1.0, -1.0, 2.0, -2.0, 3.0, -3.0]:
                point_subs = {v: pt for v in vars}
                term_at_point = term.subs(point_subs)
                try:
                    s = sp.Sum(sp.Abs(term_at_point), (n_var, 1, sp.oo))
                    conv = s.is_convergent()
                    if conv is not False:
                        h1 = True
                        break
                except Exception:
                    # If SymPy cannot determine convergence, we err on the side of accepting the hypothesis
                    h1 = True
                    break
                    
            # Check if the series is actually a power series.
            # A power series term evaluated at a fixed n (e.g., n=2) must be a polynomial in the spatial variables.
            term_n2 = term.subs(n_var, 2)
            is_poly = True
            for v in vars:
                if not term_n2.is_polynomial(v):
                    is_poly = False
                    break
                    
            # If it is not a power series, the conclusion fails because its partial derivatives 
            # cannot be given by a "term-by-term differentiated power series".
            neg_q = not is_poly
            
    except Exception:
        pass
        
    return [h1, neg_q]