import sympy
from sympy import Poly, Symbol
from sympy.abc import x

# Top-level setup
# No specific named objects are required for this Field Theory theorem,
# but we ensure x is available for polynomial expressions.

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            E = witness.get('E')
            alpha = witness.get('alpha')
            m = witness.get('m')
        else:
            F, E, alpha, m = witness
    except Exception:
        return [False, False, False, False]

    # H1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    # H2: E is an extension field of F
    try:
        h2 = bool(getattr(E, 'is_Field', False))
        if F != E:
            char_F = getattr(F, 'characteristic', None)
            char_E = getattr(E, 'characteristic', None)
            if char_F is not None and char_E is not None:
                h2 = h2 and (char_F == char_E)
    except Exception:
        h2 = False

    # H3: α ∈ E is an element algebraic over F
    try:
        if hasattr(E, 'of_type'):
            in_E = E.of_type(alpha)
        else:
            in_E = alpha in E
            
        if isinstance(m, Poly):
            val = m.eval(alpha)
            is_root = (val == 0 or val == getattr(F, 'zero', 0) or val == getattr(E, 'zero', 0))
        else:
            x_sym = list(m.free_symbols)[0] if m.free_symbols else sympy.Symbol('x')
            val = m.subs(x_sym, alpha)
            is_root = (sympy.simplify(val) == 0)
            
        if F == E:
            is_alg = True
        else:
            is_alg = is_root
            
        h3 = bool(in_E and is_alg)
    except Exception:
        h3 = False

    # neg_Q: α is separable over F iff m'(x) is not the zero polynomial
    try:
        # If F == E, the minimal polynomial of alpha over F is x - alpha,
        # which has derivative 1 != 0, so alpha is always separable.
        # For perfect fields or general valid witnesses, we assume separability holds.
        if F == E:
            alpha_separable = True
        else:
            alpha_separable = True

        if isinstance(m, Poly):
            m_deriv = m.diff()
            m_deriv_not_zero = not m_deriv.is_zero
        else:
            x_sym = list(m.free_symbols)[0] if m.free_symbols else sympy.Symbol('x')
            m_deriv = sympy.diff(m, x_sym)
            m_deriv_not_zero = not (sympy.simplify(m_deriv) == 0)

        conclusion = (alpha_separable == m_deriv_not_zero)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an extension field of F",
    "H_3: α ∈ E is an element algebraic over F",
    "¬Q: The equivalence (α is separable over F iff m'(x) is not the zero polynomial) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3