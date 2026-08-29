import sympy

n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness):
    try:
        witness = sympy.sympify(witness)
    except Exception:
        return [False, False]

    # H_1: a_n is a sequence of real numbers
    try:
        h1 = isinstance(witness, sympy.Expr) and witness.free_symbols.issubset({n})
        if h1:
            for i in range(1, 6):
                val = witness.subs(n, i).evalf()
                if not val.is_real:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # ¬Q: The series sum(a_n) does NOT converge to a real number
    try:
        s = sympy.Sum(witness, (n, 1, sympy.oo))
        conv = s.is_convergent()
        if conv is False:
            neg_q = True
        elif conv is True:
            neg_q = False
        else:
            val = s.doit()
            if val.has(sympy.oo, -sympy.oo, sympy.zoo) or val.is_real is False:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a_n is a sequence of real numbers",
    "¬Q: sum(a_n) does not converge to a real number"
]

N_HYP = 1
NEG_Q_INDEX = 1