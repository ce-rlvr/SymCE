import sympy
from sympy.abc import x, y, z, t
from sympy.polys.domains import ZZ, QQ, RR, CC, FF

# Top-level setup
# We provide standard domains and variables for constructing witness fields.
# Example witness for this conjecture: FF(2).frac_field(x)

def conditions(witness):
    """
    Check if the witness is a counterexample to the conjecture:
    "If \overline{F} is an algebraic closure of F, then \overline{F}/F is a Galois extension."
    
    A counterexample must be a field F that is NOT perfect.
    """
    # The witness might be provided as a tuple (F, F_alg) or just F.
    if isinstance(witness, tuple) and len(witness) >= 1:
        F = witness[0]
    else:
        F = witness

    try:
        # H_1: \overline{F} is an algebraic closure of F
        # This implicitly requires F to be a field. Every field has an algebraic closure.
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        # neg_Q: The field extension \overline{F}/F is NOT a Galois extension.
        # This is equivalent to saying F is NOT a perfect field.
        if not h1:
            neg_q = False
        else:
            char = getattr(F, 'characteristic', 0)
            if char == 0:
                is_perfect = True
            elif getattr(F, 'is_FiniteField', False):
                is_perfect = True
            elif getattr(F, 'is_FractionField', False):
                # A fraction field over a field of characteristic p > 0 is imperfect.
                is_perfect = False
            else:
                # Fallback: assume perfect if we cannot determine
                is_perfect = True
            
            neg_q = not is_perfect
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: \\overline{F} is an algebraic closure of F",
    "¬Q: The field extension \\overline{F}/F is not a Galois extension"
]

N_HYP = 1
NEG_Q_INDEX = 1