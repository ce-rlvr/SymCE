import sympy as sp

# Top-level setup for witness expressions
x, y, z = sp.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    Expected witness format: (U, f, vars)
      - U: a sympy Set representing the domain (e.g., sp.Interval(0, 1))
      - f: a list of sympy expressions for the function (e.g., [x])
      - vars: a list of sympy symbols used in f (e.g., [x])
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False]
            
        U, f, vars = witness
        n = len(vars)
        if n != len(f):
            return [False, False, False]
            
        if n != 1:
            # For simplicity and robustness, we only verify 1D counterexamples
            return [False, False, False]
            
        v = vars[0]
        expr = f[0]
        
        # Compute Jacobian (1x1 matrix)
        J = sp.diff(expr, v)
        detJ = J
        
        # H_1: f is C^1 on U
        h1 = False
        try:
            if J.is_polynomial(v):
                h1 = True
            else:
                num, den = J.as_numer_denom()
                roots = sp.solveset(den, v, domain=U)
                if roots.is_empty:
                    h1 = True
        except Exception:
            pass
                
        # H_2: det(Df) != 0 on U
        h2 = False
        try:
            roots = sp.solveset(detJ, v, domain=U)
            if roots.is_empty:
                h2 = True
            elif roots.is_empty is None:
                if detJ.is_constant() and detJ != 0:
                    h2 = True
        except Exception:
            if detJ.is_constant() and detJ != 0:
                h2 = True
                
        # neg_Q: f is not an open mapping
        # A mapping is open if it maps open subsets of its domain to open subsets of R^n.
        # Since U is open in the relative topology of U, if f(U) is not open in R^n, 
        # then f is not an open mapping.
        neg_q = False
        try:
            f_U = sp.image(sp.Lambda(v, expr), U)
            
            if getattr(f_U, 'is_open', None) is False:
                neg_q = True
            elif isinstance(f_U, sp.Interval):
                if not (f_U.left_open and f_U.right_open):
                    neg_q = True
            elif isinstance(f_U, sp.FiniteSet):
                if not f_U.is_empty:
                    neg_q = True
        except Exception:
            pass
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f is continuously differentiable (C^1) on U",
    "H_2: Jacobian determinant is non-zero for all x in U",
    "¬Q: f is not an open mapping (e.g., f(U) is not open in R^n)"
]

N_HYP = 2
NEG_Q_INDEX = 2