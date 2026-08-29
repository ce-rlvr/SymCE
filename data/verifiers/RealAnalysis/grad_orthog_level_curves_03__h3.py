import sympy as sp
import math

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the given witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    The witness should be a dictionary containing:
      - 'vars': tuple of sympy symbols representing the coordinates in R^n
      - 'f': sympy expression for the function f
      - 'a': tuple of coordinates for the point a
      - 'gamma': tuple of sympy expressions in terms of t for the curve gamma(t)
      - 'c': constant value that f(gamma(t)) equals
      - 't': sympy symbol for the parameter t
    """
    try:
        vars_ = witness.get('vars')
        f = witness.get('f')
        a = witness.get('a')
        gamma = witness.get('gamma')
        c = witness.get('c')
        t = witness.get('t')
        
        if not all(k in witness for k in ['vars', 'f', 'a', 'gamma', 'c', 't']):
            return [False] * 4 + [False]
            
        # H1: U is an open subset of R^n
        # We verify that the dimensions match and are > 0
        h1 = (isinstance(vars_, (list, tuple)) and 
              isinstance(a, (list, tuple)) and 
              isinstance(gamma, (list, tuple)) and 
              len(vars_) > 0 and 
              len(vars_) == len(a) == len(gamma))
              
        if not h1:
            return [False, False, False, False, False]
            
        f_sym = sp.sympify(f)
        
        # H2: f is differentiable at a
        # We check if all partial derivatives exist and are finite at a
        h2 = True
        grad_f = []
        for v in vars_:
            df = sp.diff(f_sym, v)
            val = sp.sympify(df.subs(list(zip(vars_, a))))
            if val.has(sp.nan) or val.has(sp.zoo) or val.has(sp.oo) or val.has(-sp.oo):
                h2 = False
                break
            grad_f.append(val)
            
        # H3: gamma(0) == a
        h3 = True
        for g, a_val in zip(gamma, a):
            g_sym = sp.sympify(g)
            if sp.simplify(g_sym.subs(t, 0) - a_val) != 0:
                h3 = False
                break
                
        # H4: f(gamma(t)) == c for all t in (-1, 1)
        f_gamma = f_sym.subs(dict(zip(vars_, gamma)))
        h4 = False
        diff_expr = sp.simplify(f_gamma - c)
        if diff_expr == 0:
            h4 = True
        else:
            # Fallback to numerical evaluation if symbolic simplification fails
            h4_num = True
            for test_val in [0.1, -0.1, 0.5, -0.5, 0.9, -0.9]:
                try:
                    val = float(diff_expr.subs(t, test_val))
                    if abs(val) > 1e-7:
                        h4_num = False
                        break
                except Exception:
                    h4_num = False
                    break
            h4 = h4_num
            
        # neg_Q: The dot product grad f(a) \cdot gamma'(0) is NOT equal to 0
        # This happens if the dot product is non-zero, or if gamma'(0) is undefined (nan/zoo)
        gamma_prime_0 = []
        for g in gamma:
            g_sym = sp.sympify(g)
            dg = sp.diff(g_sym, t)
            val = sp.sympify(dg.subs(t, 0))
            gamma_prime_0.append(val)
            
        dot_product = sp.sympify(sum(gf * gp for gf, gp in zip(grad_f, gamma_prime_0)))
        
        if dot_product.has(sp.nan) or dot_product.has(sp.zoo) or dot_product.has(sp.oo) or dot_product.has(-sp.oo):
            neg_q = True
        else:
            neg_q = bool(sp.simplify(dot_product) != 0)
            
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False] * 4 + [False]

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: f is differentiable at a",
    "H_3: gamma(0) = a",
    "H_4: f(gamma(t)) = c for all t in (-1, 1)",
    "¬Q: grad f(a) \cdot gamma'(0) is not equal to 0 (or is undefined)"
]

N_HYP = 4
NEG_Q_INDEX = 4