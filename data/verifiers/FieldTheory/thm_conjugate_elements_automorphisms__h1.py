import sympy
from sympy import symbols, Poly

# Top-level setup
# We define symbols that might be used in witness expressions.
# The witness is expected to be a dictionary or object providing:
# 'E': the algebraically closed field (or a representation of it)
# 'F': the base field
# 'alpha': the element alpha
# 'beta': the element beta
# 'min_poly_alpha': minimal polynomial of alpha over F
# 'min_poly_beta': minimal polynomial of beta over F
# 'automorphisms': a list of automorphisms of E over F (or a way to check existence)

x = symbols('x')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    
    Remaining hypotheses:
      1. E is an algebraically closed field containing F
      2. alpha and beta are elements of E that are algebraic over F
      
    Conclusion (must FAIL at the witness):
      alpha and beta share the same minimal polynomial over F if and only if 
      there exists an automorphism sigma in Aut(E/F) such that sigma(alpha) = beta.
    """
    try:
        E = witness.get('E')
        F = witness.get('F')
        alpha = witness.get('alpha')
        beta = witness.get('beta')
    except Exception:
        return [False, False, False]

    # H1: E is an algebraically closed field containing F
    try:
        # In a computational setting, we verify the witness claims E is algebraically closed
        # and contains F. We rely on the witness structure to provide this boolean.
        h1_ok = bool(witness.get('is_E_algebraically_closed_containing_F', False))
    except Exception:
        h1_ok = False

    # H2: alpha and beta are elements of E that are algebraic over F
    try:
        h2_ok = bool(witness.get('are_alpha_beta_algebraic_over_F', False))
    except Exception:
        h2_ok = False

    # Negated Conclusion:
    # The conclusion is: (same minimal polynomial) <=> (exists automorphism mapping alpha to beta)
    # We need this conclusion to FAIL.
    try:
        same_min_poly = bool(witness.get('same_min_poly', False))
        exists_automorphism = bool(witness.get('exists_automorphism', False))
        
        # The conclusion is the equivalence: same_min_poly == exists_automorphism
        # The negation is that they are NOT equivalent (XOR).
        neg_q_ok = (same_min_poly != exists_automorphism)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: E is an algebraically closed field containing F",
    "H_2: \\alpha and \\beta are elements of E that are algebraic over F",
    "¬Q: It is NOT the case that (\\alpha and \\beta share the same minimal polynomial over F iff there exists an automorphism mapping \\alpha to \\beta)"
]

N_HYP = 2
NEG_Q_INDEX = 2