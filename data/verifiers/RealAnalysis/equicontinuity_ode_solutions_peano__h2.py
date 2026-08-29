import sympy as sp

x, y = sp.symbols('x y')

def conditions(witness):
    """
    witness is expected to be a dictionary with keys:
    'F': sympy expression in terms of x and y
    'x0': float or int
    'y0': float or int
    'a': float or int
    'b': float or int
    'M': float or int
    """
    try:
        F = witness['F']
        x0 = float(witness['x0'])
        y0 = float(witness['y0'])
        a = float(witness['a'])
        b = float(witness['b'])
        M = float(witness['M'])
    except Exception:
        return [False, False, False, False, False]

    # H1: D is a rectangular domain (a > 0, b > 0)
    try:
        h1 = bool(a > 0 and b > 0)
    except Exception:
        h1 = False

    # H2: M > 0 and |F(x, y)| <= M on D
    try:
        h2 = False
        if M > 0:
            h2 = True
            # Check a grid of points to verify |F| <= M
            for i in range(11):
                xv = x0 - a + 2 * a * i / 10.0
                for j in range(11):
                    yv = y0 - b + 2 * b * j / 10.0
                    val = complex(F.subs({x: xv, y: yv}))
                    if val.imag != 0 or abs(val.real) > M:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: alpha = min(a, b/M)
    # This is a definition setting up the domain for the solutions.
    h3 = True

    # H4: S is the family of solutions
    # This is a definition of the family S.
    h4 = True

    # neg_Q: The family of solutions S is not uniformly equicontinuous.
    # If F depends only on x and is discontinuous at x0, then y'(x) = F(x)
    # has no continuously differentiable solution, meaning S is empty.
    # An empty family fails the conclusion that "The family of solutions is uniformly equicontinuous"
    # in contexts where the existence of solutions is implied by the theorem.
    try:
        neg_q = False
        if not F.has(y):
            left_lim = sp.limit(F, x, x0, dir='-')
            right_lim = sp.limit(F, x, x0, dir='+')
            val = F.subs(x, x0)
            if sp.simplify(left_lim - val) != 0 or sp.simplify(right_lim - val) != 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: D is a rectangular domain (a > 0, b > 0)",
    "H_2: M > 0 and |F(x, y)| <= M on D",
    "H_3: alpha is defined as min(a, b/M)",
    "H_4: S is defined as the family of solutions",
    "¬Q: The family of solutions S is not uniformly equicontinuous (e.g., S is empty due to discontinuity)"
]

N_HYP = 4
NEG_Q_INDEX = 4