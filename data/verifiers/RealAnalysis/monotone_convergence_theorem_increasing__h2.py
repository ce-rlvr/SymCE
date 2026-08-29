import sympy

n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    try:
        witness = sympy.sympify(witness)
    except Exception:
        return [False, False, False]

    # H1: (a_n) is a sequence of real numbers
    try:
        h1 = True
        for i in range(1, 20):
            val = complex(witness.subs(n, i).evalf())
            if abs(val.imag) > 1e-9:
                h1 = False
                break
    except Exception:
        h1 = False

    # H2: (a_n) is bounded above
    try:
        L = sympy.limit(witness, n, sympy.oo)
        if L == sympy.oo:
            h2 = False
        elif isinstance(L, sympy.AccumBounds) and L.max == sympy.oo:
            h2 = False
        elif L == sympy.nan or (not L.is_number and not isinstance(L, sympy.AccumBounds)):
            h2 = True
            max_val = -float('inf')
            for i in range(1, 100):
                try:
                    val = float(witness.subs(n, i).evalf())
                    if val > max_val:
                        max_val = val
                except Exception:
                    pass
            for i in [10**3, 10**3+1, 10**4, 10**4+1, 10**5, 10**5+1]:
                try:
                    val = float(witness.subs(n, i).evalf())
                    if val > max_val + 100:
                        h2 = False
                        break
                except Exception:
                    pass
        else:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: The sequence (a_n) does NOT converge to a real number
    try:
        L = sympy.limit(witness, n, sympy.oo)
        if isinstance(L, sympy.AccumBounds):
            neg_q = True
        elif L in [sympy.oo, -sympy.oo, sympy.zoo, sympy.nan]:
            neg_q = True
        elif L.is_real and L.is_finite:
            neg_q = False
        else:
            try:
                float(L)
                neg_q = False
            except Exception:
                neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (a_n) is a sequence of real numbers",
    "H_2: (a_n) is bounded above",
    "¬Q: The sequence (a_n) does not converge to a real number"
]

N_HYP = 2
NEG_Q_INDEX = 2