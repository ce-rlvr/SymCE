import sympy as sp

# Top-level setup for the witness namespace
n = sp.Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should be a tuple of two expressions or functions (a_n, b_n).
    """
    try:
        # Handle both callable functions and SymPy expressions/strings
        if callable(witness[0]):
            a = witness[0](n)
            b = witness[1](n)
        else:
            a, b = witness
            
        a = sp.sympify(a)
        b = sp.sympify(b)
    except Exception:
        return [False, False, False]

    # H_1: 0 <= a_n <= b_n for all n >= 1
    h1_ok = True
    try:
        # Fast symbolic check if possible
        if a.is_nonnegative and (b - a).is_nonnegative:
            h1_ok = True
        else:
            # Fallback to numerical check for the first 1000 terms
            for i in range(1, 1001):
                av = float(a.subs(n, i).evalf())
                bv = float(b.subs(n, i).evalf())
                if not (-1e-12 <= av <= bv + 1e-12):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H_2: The series \sum_{n=1}^\infty b_n converges
    h2_ok = False
    try:
        s_b = sp.Sum(b, (n, 1, sp.oo))
        conv_b = s_b.is_convergent()
        if conv_b is not None:
            h2_ok = bool(conv_b)
        else:
            # Fallback necessary condition: limit must be 0
            if sp.limit(b, n, sp.oo) != 0:
                h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The series \sum_{n=1}^\infty a_n diverges (conclusion fails)
    neg_q_ok = False
    try:
        s_a = sp.Sum(a, (n, 1, sp.oo))
        conv_a = s_a.is_convergent()
        if conv_a is not None:
            neg_q_ok = not bool(conv_a)
        else:
            # Fallback necessary condition: if limit is not 0, it diverges
            if sp.limit(a, n, sp.oo) != 0:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: 0 <= a_n <= b_n for all n >= 1",
    "H_2: The series \\sum_{n=1}^\\infty b_n converges",
    "¬Q: The series \\sum_{n=1}^\\infty a_n does not converge"
]

N_HYP = 2
NEG_Q_INDEX = 2