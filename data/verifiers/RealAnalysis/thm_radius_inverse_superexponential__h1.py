import sympy

n = sympy.Symbol('n', integer=True, positive=True)
x = sympy.Symbol('x')

def conditions(witness):
    """
    Check if the witness (a sympy expression for a_n) satisfies the negated conclusion.
    The conclusion is that the radius of convergence is infinity.
    The negated conclusion is that the radius of convergence is NOT infinity.
    """
    neg_q = False
    try:
        # Try the root test: L = lim_{n -> oo} |a_n|^(1/n)
        # Radius of convergence R = 1 / L
        # R = oo iff L = 0
        root_limit = sympy.limit(sympy.Abs(witness)**(1/n), n, sympy.oo)
        
        if root_limit == 0:
            neg_q = False
        elif root_limit == sympy.oo or (hasattr(root_limit, 'is_number') and root_limit.is_number and not root_limit.has(sympy.nan)):
            neg_q = True
        else:
            # Fallback to the ratio test: L = lim_{n -> oo} |a_n / a_{n+1}|
            # Radius of convergence R = L
            # R = oo iff L = oo
            ratio_limit = sympy.limit(sympy.Abs(witness / witness.subs(n, n + 1)), n, sympy.oo)
            if ratio_limit == sympy.oo:
                neg_q = False
            elif ratio_limit == 0 or (hasattr(ratio_limit, 'is_number') and ratio_limit.is_number and not ratio_limit.has(sympy.nan)):
                neg_q = True
    except Exception:
        pass

    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: The radius of convergence of the power series is not infinity"
]

N_HYP = 0
NEG_Q_INDEX = 0