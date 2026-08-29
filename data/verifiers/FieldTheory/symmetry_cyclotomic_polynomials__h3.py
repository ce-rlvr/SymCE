import sympy
from sympy import cyclotomic_poly, totient
from sympy.abc import x

# Standard algebra objects relevant to the domain
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness can be an integer `n` or a tuple `(n, P)` where `P` is a polynomial.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                n, P = witness
            else:
                return [False, False, False]
        else:
            n = witness
            P = cyclotomic_poly(int(n), x)
    except Exception:
        return [False, False, False]
        
    # H_1: n is an integer strictly greater than 1
    try:
        h1 = (int(n) == n) and (n > 1)
    except Exception:
        h1 = False
        
    # H_2: Phi_n(x) is the n-th cyclotomic polynomial
    try:
        if hasattr(P, 'as_expr'):
            P_expr = P.as_expr()
        else:
            P_expr = P
            
        var = x
        if hasattr(P_expr, 'free_symbols') and len(P_expr.free_symbols) == 1:
            var = list(P_expr.free_symbols)[0]
            
        expected_P = cyclotomic_poly(int(n), var)
        diff_h2 = sympy.expand(P_expr - expected_P)
        h2 = bool(diff_h2 == 0)
    except Exception:
        h2 = False
        
    # ¬Q: The polynomial does NOT satisfy the identity x^phi(n) Phi_n(1/x) = Phi_n(x)
    try:
        d = totient(int(n))
        lhs = sympy.expand(var**d * P_expr.subs(var, 1/var))
        rhs = sympy.expand(P_expr)
        diff_q = sympy.expand(lhs - rhs)
        neg_q = bool(diff_q != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: Phi_n(x) is the n-th cyclotomic polynomial",
    "¬Q: The polynomial does not satisfy the identity x^phi(n) Phi_n(1/x) = Phi_n(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2