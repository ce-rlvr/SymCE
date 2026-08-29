import sympy
from sympy.abc import *
import z3

def conditions(witness):
    try:
        # Extract witness components
        K = witness.get('K', '')
        X = witness.get('X', '')
        Y = witness.get('Y', '')
        C = witness.get('C', '')
        f_val = witness.get('f', None)
        
        # H1: X and Y are algebraic varieties over K
        # We require K to be a non-algebraically closed field like R
        # and X, Y to be affine spaces, with Y = A^1 for tractability
        K_str = str(K).upper()
        h1 = K_str in ['R', 'REAL', 'REALS', 'R1'] or 'REAL' in K_str
        
        X_str = str(X).upper()
        Y_str = str(Y).upper()
        h1 = h1 and 'A' in X_str
        h1 = h1 and Y_str in ['A1', 'A^1', 'A_1']
        
        # H2: f is a morphism of varieties
        # For affine spaces, a morphism is given by polynomials
        f = sympy.sympify(f_val)
        h2 = isinstance(f, sympy.Expr) and f.is_polynomial()
        
        # H3: C is a constructible set in X
        # For simplicity, we require C to be the whole space X (which is trivially constructible)
        C_str = str(C).strip().upper()
        h3 = (C_str == X_str.strip()) or (C_str == 'X')
        
        # neg_Q: f(C) is not constructible in Y
        neg_q = False
        if h1 and h2 and h3:
            free_vars = list(f.free_symbols)
            if not free_vars:
                is_constant = True
            else:
                # Check if all partial derivatives are zero
                is_constant = all(sympy.diff(f, v) == 0 for v in free_vars)
                
            if not is_constant:
                # In A^1_R, constructible sets are finite or co-finite.
                # The image of R^n under a polynomial is an interval.
                # An interval is finite iff it's a point (f is constant).
                # An interval is co-finite iff it's the whole R (f is surjective).
                # Thus, the image is NOT constructible iff f is NOT constant AND f is NOT surjective.
                
                poly = sympy.Poly(f, *free_vars)
                z3_vars = {v.name: z3.Real(v.name) for v in free_vars}
                
                terms = []
                for monom, coeff in zip(poly.monoms(), poly.coeffs()):
                    if coeff.is_Integer:
                        c = z3.RealVal(int(coeff))
                    elif coeff.is_Rational:
                        c = z3.RealVal(coeff.p) / z3.RealVal(coeff.q)
                    else:
                        c = z3.RealVal(float(coeff))
                        
                    term = c
                    for var, exp in zip(poly.gens, monom):
                        if exp > 0:
                            term = term * (z3_vars[var.name] ** int(exp))
                    terms.append(term)
                
                if not terms:
                    z3_f = z3.RealVal(0)
                elif len(terms) == 1:
                    z3_f = terms[0]
                else:
                    z3_f = z3.Sum(*terms)
                    
                y_var = z3.Real('y_target')
                x_z3_vars = list(z3_vars.values())
                
                solver = z3.Solver()
                solver.set("timeout", 2000)
                
                # Check surjectivity: ForAll(y, Exists(x, f(x) == y))
                # Negation: Exists(y, ForAll(x, f(x) != y))
                solver.add(z3.ForAll(x_z3_vars, z3_f != y_var))
                
                result = solver.check()
                if result == z3.sat:
                    # There is a y_target not in the image -> not surjective -> not constructible
                    neg_q = True
                elif result == z3.unsat:
                    # Surjective -> image is R -> constructible
                    neg_q = False
                else:
                    # Timeout or unknown -> fail safe
                    neg_q = False
                    
    except Exception:
        return [False, False, False, False]
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X and Y are algebraic varieties over K",
    "H_2: f: X -> Y is a morphism of varieties",
    "H_3: C is a constructible set in X",
    "¬Q: The image f(C) is not a constructible set in Y"
]

N_HYP = 3
NEG_Q_INDEX = 3