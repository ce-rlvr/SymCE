import sympy

# Top-level setup: named object bindings that the witness expression may reference.
# We provide scalar variables for 1D inputs, and vector components for 2D inputs.
x, y, h, k = sympy.symbols('x y h k', real=True)
x1, x2, y1, y2 = sympy.symbols('x1 x2 y1 y2', real=True)
h1, h2, k1, k2 = sympy.symbols('h1 h2 k1 k2', real=True)

def conditions(witness):
    try:
        B = sympy.sympify(witness)
        
        # Determine which variables are used to compute the total derivative correctly
        free_vars = B.free_symbols
        
        if any(v in free_vars for v in (x1, x2, y1, y2)):
            # 2D case
            dB_dx1 = sympy.diff(B, x1)
            dB_dx2 = sympy.diff(B, x2)
            dB_dy1 = sympy.diff(B, y1)
            dB_dy2 = sympy.diff(B, y2)
            
            total_deriv = dB_dx1 * h1 + dB_dx2 * h2 + dB_dy1 * k1 + dB_dy2 * k2
            expected = B.subs({y1: k1, y2: k2}) + B.subs({x1: h1, x2: h2})
        else:
            # 1D case (default)
            dB_dx = sympy.diff(B, x)
            dB_dy = sympy.diff(B, y)
            
            total_deriv = dB_dx * h + dB_dy * k
            expected = B.subs(y, k) + B.subs(x, h)
            
        diff_expr = sympy.simplify(total_deriv - expected)
        
        # Check if the difference is zero (handling both scalars and matrices)
        if hasattr(diff_expr, 'is_zero_matrix') and diff_expr.is_zero_matrix:
            is_equal = True
        elif diff_expr == 0:
            is_equal = True
        else:
            # Fallback to expand if simplify missed something
            diff_expr = sympy.expand(diff_expr)
            if hasattr(diff_expr, 'is_zero_matrix') and diff_expr.is_zero_matrix:
                is_equal = True
            elif diff_expr == 0:
                is_equal = True
            else:
                is_equal = False
                
        # The conclusion is that B is differentiable everywhere AND the derivative matches the formula.
        # If the formula does not hold, the conclusion fails (neg_Q is True).
        neg_Q = not is_equal
        
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The map B is not differentiable everywhere, or its total derivative at (x, y) evaluated at (h, k) is not B(x, k) + B(h, y)"
]

N_HYP = 0
NEG_Q_INDEX = 0