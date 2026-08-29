import sympy
from sympy import cyclotomic_poly, discriminant
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    Remaining hypothesis:
      H_1: p is an odd prime number
      
    Conclusion to falsify:
      Q: The discriminant of Q(zeta_p) over Q is (-1)^{(p-1)/2} p^{p-2}.
    """
    # Check H_1: p is an odd prime number
    try:
        p_sym = sympy.sympify(witness)
        if not p_sym.is_Integer:
            h1_ok = False
        else:
            p = int(p_sym)
            h1_ok = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1_ok = False

    # Check ¬Q: The discriminant of Q(zeta_p) over Q is NOT (-1)^{(p-1)/2} p^{p-2}
    try:
        p_sym = sympy.sympify(witness)
        if not p_sym.is_Integer:
            neg_q_ok = False
        else:
            p = int(p_sym)
            # The ring of integers of Q(zeta_p) is Z[zeta_p].
            # Thus, the discriminant of the field over Q is exactly the discriminant 
            # of the minimal polynomial of zeta_p, which is the p-th cyclotomic polynomial.
            poly = cyclotomic_poly(p, x)
            disc = discriminant(poly, x)
            
            expected_disc = ((-1)**((p - 1) // 2)) * (p**(p - 2))
            
            neg_q_ok = bool(disc != expected_disc)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "¬Q: The discriminant of Q(zeta_p) over Q is not (-1)^{(p-1)/2} p^{p-2}"
]

N_HYP = 1
NEG_Q_INDEX = 1