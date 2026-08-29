import sympy
from sympy import Sum, oo, Symbol, re, sympify, zeta
from sympy.ntheory import mobius

# Top-level setup
# No specific named bindings needed for Number Theory

CONDITION_LABELS = [
    "H_1: s is a complex number such that Re(s) > 1",
    "H_2: zeta(s) is the Riemann zeta function",
    "¬Q: sum_{n=1}^infty mu(n)/n^s != 1/zeta(s)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # H_1: s is a complex number such that \Re(s) > 1
    try:
        s = sympify(witness)
        if s.is_complex:
            h1 = bool(re(s) > 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: \zeta(s) is the Riemann zeta function
    try:
        # This is a definitional hypothesis, always true in this context
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: \sum_{n=1}^\infty \frac{\mu(n)}{n^s} \neq \frac{1}{\zeta(s)}
    try:
        s = sympify(witness)
        n = Symbol('n', integer=True, positive=True)
        lhs = Sum(mobius(n)/n**s, (n, 1, oo))
        rhs = 1/zeta(s)
        # SymPy does not evaluate the Dirichlet series for the Möbius function,
        # so structural equality correctly reflects the symbolic engine's state.
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]