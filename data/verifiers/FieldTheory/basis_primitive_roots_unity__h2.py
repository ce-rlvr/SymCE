import sympy
from sympy.abc import x

# Top-level setup: 
# x is used as the generator of the cyclotomic field Q(zeta_n)
# The witness should be a tuple (n, S) where S is a list of expressions in x.

def conditions(witness) -> list[bool]:
    try:
        n, S = witness
    except Exception:
        return [False, False]
        
    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion fails
    # Conclusion: S forms a Q-basis for Q(zeta_n) iff n is square-free
    try:
        P = False
        if isinstance(S, (list, tuple, set)):
            totient = sympy.totient(n)
            if len(S) == totient:
                Phi = sympy.cyclotomic_poly(n, x)
                rows = []
                valid_elements = True
                for s in S:
                    try:
                        expr = sympy.sympify(s)
                        poly_expr = sympy.Poly(expr, x, domain='QQ')
                        _, rem = poly_expr.div(sympy.Poly(Phi, x, domain='QQ'))
                        coeffs = rem.all_coeffs()
                        # Pad coefficients to match the degree of the field extension (totient)
                        coeffs = [0]*(totient - len(coeffs)) + coeffs
                        rows.append(coeffs)
                    except Exception:
                        valid_elements = False
                        break
                if valid_elements:
                    M = sympy.Matrix(rows)
                    P = (M.det() != 0)
                    
        # Check if n is square-free
        factors = sympy.factorint(n)
        Q = True
        for p, e in factors.items():
            if e > 1:
                Q = False
                break
                
        # The conclusion is P <-> Q. It fails when P != Q.
        neg_q = (P != Q)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: S forms a Q-basis for Q(zeta_n) iff n is square-free is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1