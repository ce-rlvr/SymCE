import sympy

n = sympy.Symbol('n', integer=True, nonnegative=True)

def conditions(witness) -> list[bool]:
    try:
        # Try root test: lim_{n \to \infty} |a_n|^{1/n}
        root_limit = sympy.limit(sympy.Abs(witness)**(1/n), n, sympy.oo)
        if not isinstance(root_limit, sympy.Limit) and root_limit is not sympy.nan:
            neg_q = (root_limit != 0)
            return [bool(neg_q)]
    except Exception:
        pass

    try:
        # Try ratio test: lim_{n \to \infty} |a_{n+1} / a_n|
        ratio_limit = sympy.limit(sympy.Abs(witness.subs(n, n+1) / witness), n, sympy.oo)
        if not isinstance(ratio_limit, sympy.Limit) and ratio_limit is not sympy.nan:
            neg_q = (ratio_limit != 0)
            return [bool(neg_q)]
    except Exception:
        pass

    try:
        # Fallback: evaluate at n=100, 101, 200, 201, 300, 301
        # If the sequence doesn't decay to 0, the radius of convergence cannot be infinity.
        vs = []
        for i in [100, 101, 200, 201, 300, 301]:
            vs.append(float(sympy.Abs(witness.subs(n, i))))
        if max(vs[0], vs[1]) > 1e-10 and max(vs[2], vs[3]) > 1e-10 and max(vs[4], vs[5]) > 1e-10:
            return [True]
    except OverflowError:
        # If it overflows float, it's growing very fast, so R is definitely not infinity
        return [True]
    except Exception:
        pass

    return [False]

CONDITION_LABELS = [
    "¬Q: The radius of convergence is not infinity"
]
N_HYP = 0
NEG_Q_INDEX = 0