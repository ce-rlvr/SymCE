import sympy

n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    try:
        witness = sympy.sympify(witness)
    except Exception:
        return [False]

    if witness == 0:
        return [True]

    try:
        ratio = sympy.simplify(sympy.Abs(witness.subs(n, n+1) / witness))
        L_ratio = sympy.limit(ratio, n, sympy.oo)
        if L_ratio == sympy.oo:
            return [False]
        if not L_ratio.has(sympy.nan):
            return [True]
    except Exception:
        pass

    try:
        root = sympy.Abs(witness)**(1/n)
        L_root = sympy.limit(root, n, sympy.oo)
        if L_root == sympy.oo:
            return [False]
        if not L_root.has(sympy.nan):
            return [True]
    except Exception:
        pass

    return [False]

CONDITION_LABELS = [
    "¬Q: The radius of convergence of the power series is not equal to 0"
]
N_HYP = 0
NEG_Q_INDEX = 0