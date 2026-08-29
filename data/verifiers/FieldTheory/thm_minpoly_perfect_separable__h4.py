import sympy
from sympy import QQ, Poly
from sympy.abc import x

# Top-level setup
# (No specific named groups or matrices needed for this field theory conjecture)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    "Separability of Minimal Polynomials over Perfect Fields" (with missing minimal polynomial hypothesis).
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F', QQ)
            K = witness.get('K', QQ)
            alpha = witness.get('alpha', 1)
            m = witness.get('m')
            E = witness.get('E', QQ)
        else:
            # If witness is just the polynomial m(x)
            m = witness
            F = QQ
            K = QQ
            alpha = 1
            E = QQ
            
        if not isinstance(m, Poly):
            m = Poly(m, x)
    except Exception:
        return [False] * 5

    # H_1: F is a perfect field
    try:
        # QQ is a perfect field (characteristic 0)
        h1 = (F == QQ) or type(F).__name__ == 'FiniteField'
    except Exception:
        h1 = False

    # H_2: K is an extension field of F
    try:
        h2 = (K == F)
    except Exception:
        h2 = False

    # H_3: \alpha \in K is algebraic over F
    try:
        if K == QQ and F == QQ:
            # Any rational number is algebraic over QQ
            h3 = isinstance(alpha, (int, float, sympy.Integer, sympy.Float, sympy.Rational))
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: E is a splitting field of m(x) over F
    try:
        if F == QQ and E == QQ:
            roots_dict = m.roots()
            # Check if all roots are in QQ (i.e., rational)
            all_rational = all(
                getattr(r, 'is_rational', False) or isinstance(r, (int, sympy.Integer, sympy.Rational)) 
                for r in roots_dict.keys()
            )
            # E is a splitting field if m(x) splits completely into linear factors in E
            h4 = (sum(roots_dict.values()) == m.degree()) and (m.degree() >= 1) and all_rational
        else:
            h4 = False
    except Exception:
        h4 = False

    # ¬Q: All roots of m(x) in E have multiplicity 1 (Negated: at least one root has multiplicity > 1)
    try:
        roots_dict = m.roots()
        neg_q = any(mult > 1 for root, mult in roots_dict.items())
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a perfect field",
    "H_2: K is an extension field of F",
    "H_3: alpha in K is algebraic over F",
    "H_4: E is a splitting field of m(x) over F",
    "¬Q: m(x) has a root in E with multiplicity > 1"
]

N_HYP = 4
NEG_Q_INDEX = 4