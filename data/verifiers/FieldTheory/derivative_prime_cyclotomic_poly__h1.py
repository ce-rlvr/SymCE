import sympy
from sympy import Symbol, diff, rem, cyclotomic_poly

# Top-level setup
# No specific named objects needed for this number theory / polynomial conjecture.

def conditions(witness):
    try:
        p = int(witness)
        if p != witness:
            return [False, False, False, False]
        if p < 2:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: \zeta_p is a primitive p-th root of unity in \mathbb{C}
    # This is a definition that holds for any integer p >= 2.
    h1 = True
    
    # H_2: \Phi_p(x) is the p-th cyclotomic polynomial
    # This is a definition that holds for any integer p >= 2.
    h2 = True
    
    # H_3: \Phi_p'(x) is the formal derivative of \Phi_p(x)
    # This is a definition that holds for any integer p >= 2.
    h3 = True
    
    try:
        x = Symbol('x')
        phi = cyclotomic_poly(p, x)
        phi_prime = diff(phi, x)
        
        # Check if \Phi_p'(\zeta_p) = p / (\zeta_p * (\zeta_p - 1))
        # This is equivalent to: \zeta_p * (\zeta_p - 1) * \Phi_p'(\zeta_p) = p
        # As polynomials, x * (x - 1) * \Phi_p'(x) \equiv p \pmod{\Phi_p(x)}
        expr = x * (x - 1) * phi_prime - p
        remainder = rem(expr, phi, x)
        
        # neg_q is True if the conclusion FAILS (i.e., remainder is not zero)
        neg_q = bool(sympy.simplify(remainder) != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: \\zeta_p is a primitive p-th root of unity in \\mathbb{C}",
    "H_2: \\Phi_p(x) is the p-th cyclotomic polynomial",
    "H_3: \\Phi_p'(x) is the formal derivative of \\Phi_p(x)",
    "¬Q: \\Phi_p'(\\zeta_p) \\neq \\frac{p}{\\zeta_p(\\zeta_p - 1)}"
]

N_HYP = 3
NEG_Q_INDEX = 3