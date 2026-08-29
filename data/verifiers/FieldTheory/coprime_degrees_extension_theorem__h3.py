import sympy
from sympy import Rational
from sympy.polys.numberfields import primitive_element
from sympy.abc import x

def get_degree(elements):
    """
    Computes the degree of the field extension Q(elements) over Q.
    Returns the degree as an integer, or None if the elements are not algebraic.
    """
    try:
        elem, poly = primitive_element(elements, x)
        return poly.degree()
    except Exception:
        return None

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Coprime Degrees Extension Theorem.
    The witness should be a tuple or list of SymPy algebraic expressions:
      - (a, b) representing F = Q, K = Q(a), L = Q(b)
      - (a, b, f) representing F = Q(f), K = F(a), L = F(b)
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                a, b = witness
                f = sympy.S.Zero
            elif len(witness) == 3:
                a, b, f = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: K/F and L/F are finite field extensions
    try:
        deg_F = get_degree([f])
        deg_K_over_Q = get_degree([f, a])
        deg_L_over_Q = get_degree([f, b])
        deg_KL_over_Q = get_degree([f, a, b])
        
        if None in (deg_F, deg_K_over_Q, deg_L_over_Q, deg_KL_over_Q):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: K and L are contained in a common field
    # In our representation, all valid algebraic numbers are contained in the complex numbers C.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails
    # Conclusion: [KL:F] = [K:F][L:F] and K \cap L = F.
    # Note: [KL:F] = [K:F][L:F] mathematically implies K \cap L = F.
    # Thus, the conclusion holds iff [KL:F] == [K:F][L:F].
    try:
        if h1:
            deg_K_over_F = Rational(deg_K_over_Q, deg_F)
            deg_L_over_F = Rational(deg_L_over_Q, deg_F)
            deg_KL_over_F = Rational(deg_KL_over_Q, deg_F)
            
            conclusion = (deg_KL_over_F == deg_K_over_F * deg_L_over_F)
            neg_q = not conclusion
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K/F and L/F are finite field extensions",
    "H_2: K and L are contained in a common field",
    "¬Q: deg(KL/F) != deg(K/F)*deg(L/F) or K intersect L != F"
]

N_HYP = 2
NEG_Q_INDEX = 2