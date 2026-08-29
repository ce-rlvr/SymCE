import sympy
from sympy import Symbol, cos, pi, minpoly, cancel
from sympy.ntheory import totient
from sympy.polys import cyclotomic_poly

# Top-level setup
# No specific named objects required for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        if n != witness:
            return [False, False, False]
        if n < 1:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: Phi_n(x) is the n-th cyclotomic polynomial
    # (This is a definition that holds for any positive integer n)
    h1 = True
    
    # H_2: Psi_n(x) is the minimal polynomial of 2 cos(2pi/n) over Q
    # (This is a definition that holds for any positive integer n)
    h2 = True
    
    try:
        x = Symbol('x')
        phi_n = totient(n)
        
        # Compute Psi_n(x)
        psi_n = minpoly(2 * cos(2 * pi / n), x)
        deg_psi = sympy.degree(psi_n, x)
        
        # Check the conclusion
        if deg_psi != phi_n / 2:
            q = False
        else:
            # Compute Phi_n(x)
            Phi_n = cyclotomic_poly(n, x)
            
            # Evaluate x^{phi(n)/2} * Psi_n(x + x^{-1})
            half_phi = phi_n // 2
            expr = (x**half_phi) * psi_n.subs(x, x + 1/x)
            
            # Check if Phi_n(x) == expr
            diff = cancel(Phi_n - expr)
            q = (diff == 0)
            
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Phi_n(x) is the n-th cyclotomic polynomial",
    "H_2: Psi_n(x) is the minimal polynomial of 2 cos(2pi/n) over Q",
    "¬Q: The degree of Psi_n(x) is not phi(n)/2, or it does not satisfy Phi_n(x) = x^{phi(n)/2} Psi_n(x + x^{-1})"
]

N_HYP = 2
NEG_Q_INDEX = 2