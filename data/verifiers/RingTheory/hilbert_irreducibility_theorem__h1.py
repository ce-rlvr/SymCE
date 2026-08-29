import sympy
from sympy import Poly, factor_list, degree_list, Expr, Symbol

# Top-level setup
t, t1, t2, t3 = sympy.symbols('t t1 t2 t3')
c, c1, c2, c3 = sympy.symbols('c c1 c2 c3')
x, x1, x2, x3 = sympy.symbols('x x1 x2 x3')
y, z = sympy.symbols('y z')

def conditions(witness) -> list[bool]:
    try:
        # The witness can be a tuple (f, T_vars, X_vars) or just an expression f.
        if isinstance(witness, tuple) and len(witness) == 3:
            f, T_vars, X_vars = witness
        elif isinstance(witness, Expr):
            f = witness
            symbols = list(f.free_symbols)
            # Guess the partition of variables based on standard naming conventions
            T_vars = [s for s in symbols if s.name.startswith('t') or s.name.startswith('c')]
            X_vars = [s for s in symbols if s not in T_vars]
            # Fallback if no t/c variables are found but multiple variables exist
            if not T_vars and len(X_vars) >= 2:
                T_vars = [X_vars[0]]
                X_vars = X_vars[1:]
        else:
            return [False]
            
        if not T_vars or not X_vars:
            return [False]
            
        # Ensure all free symbols in f are accounted for in the variable lists
        if not set(f.free_symbols).issubset(set(T_vars).union(set(X_vars))):
            return [False]
            
        # Factor the polynomial over the rationals
        factors = factor_list(f)[1]
        
        valid_factors_count = 0
        for base, exp in factors:
            # Check if the factor has positive degree in the X variables
            deg_X = sum(degree_list(base, *X_vars))
            if deg_X > 0:
                if len(T_vars) == 1:
                    # If there is only 1 parameter, any non-zero polynomial coefficient in T 
                    # has only finitely many roots. Thus the factor has positive degree in X 
                    # for all but finitely many parameter choices.
                    valid_factors_count += exp
                else:
                    # For multiple parameters, we ensure there is at least one term with 
                    # positive degree in X whose coefficient is a non-zero constant.
                    # This guarantees the factor NEVER becomes a constant polynomial in X.
                    poly_x = Poly(base, *X_vars)
                    has_constant_coeff = False
                    for degrees, coeff in poly_x.terms():
                        if sum(degrees) > 0:
                            coeff_expr = sympy.sympify(coeff)
                            if not coeff_expr.free_symbols.intersection(set(T_vars)) and coeff_expr != 0:
                                has_constant_coeff = True
                                break
                    if has_constant_coeff:
                        valid_factors_count += exp
                        
        # If f factors into at least 2 valid components, then f(c, X) is reducible 
        # for all but at most finitely many choices of c. Thus there do NOT exist 
        # infinitely many k-tuples where it is irreducible.
        neg_q = bool(valid_factors_count >= 2)
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: There do not exist infinitely many k-tuples of integers such that f is irreducible"
]
N_HYP = 0
NEG_Q_INDEX = 0