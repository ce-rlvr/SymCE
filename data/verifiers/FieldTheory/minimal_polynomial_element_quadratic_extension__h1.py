import sympy as sp
from sympy import Poly, Matrix, zeros, eye
from sympy.abc import x

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the false conjecture.
    The witness should be a tuple (P_expr, A_expr) where:
      - P_expr is an irreducible polynomial in x over QQ defining the field extension E = QQ[x]/(P(x)).
      - A_expr is a polynomial in x representing the element alpha in E.
    """
    try:
        P_expr, A_expr = witness
        
        # Allow string inputs for convenience
        if isinstance(P_expr, str):
            P_expr = sp.sympify(P_expr)
        if isinstance(A_expr, str):
            A_expr = sp.sympify(A_expr)
            
        P = Poly(P_expr, x, domain='QQ')
        A = Poly(A_expr, x, domain='QQ')
        
        # E/F must be a valid field extension, so P must be irreducible over F (QQ)
        if not P.is_irreducible:
            return [False, False]
            
        n = P.degree()
        if n < 1:
            return [False, False]
            
        # Reduce alpha modulo P to get its canonical representation in E
        A_mod = A % P
        
        # H_1: alpha is an element of E that is not in F
        # This means its canonical polynomial representation has degree > 0
        h1 = A_mod.degree() > 0
        
        # Compute the matrix of the multiplication-by-alpha map over the basis {1, x, ..., x^{n-1}}
        M = zeros(n, n)
        for j in range(n):
            poly_j = (Poly(x**j, x, domain='QQ') * A_mod) % P
            coeffs = poly_j.all_coeffs()
            # all_coeffs returns coefficients from highest degree to 0
            coeffs = [0]*(n - len(coeffs)) + coeffs
            coeffs = coeffs[::-1] # Reverse to match the basis order 1, x, ..., x^{n-1}
            for i in range(n):
                M[i, j] = coeffs[i]
                
        # Trace and Norm of alpha in E/F
        tr = M.trace()
        norm = M.det()
        
        # The conclusion claims the minimal polynomial of alpha over F is x^2 - Tr(alpha)x + N(alpha).
        # Since alpha is not in F, its minimal polynomial must have degree >= 2.
        # Thus, x^2 - Tr(alpha)x + N(alpha) is the minimal polynomial if and only if it annihilates alpha.
        # We check if M^2 - Tr(alpha)M + N(alpha)I == 0.
        I = eye(n)
        eval_poly = M**2 - tr*M + norm*I
        
        # neg_Q: The conclusion FAILS (the minimal polynomial is NOT x^2 - Tr(alpha)x + N(alpha))
        neg_q = not eval_poly.is_zero_matrix
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: alpha is an element of E that is not in F",
    "¬Q: The minimal polynomial of alpha over F is not x^2 - Tr_{E/F}(alpha)x + N_{E/F}(alpha)"
]

N_HYP = 1
NEG_Q_INDEX = 1