import sympy
from sympy.calculus.util import continuous_domain

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "Every continuous function on R is uniformly continuous on R."
    """
    # Handle callable witness
    if callable(witness):
        try:
            f = witness(x)
        except Exception:
            f = witness
    else:
        f = witness

    # Ensure f is a sympy expression
    try:
        f = sympy.sympify(f)
    except Exception:
        pass

    # Determine the symbol to use
    free_syms = f.free_symbols if hasattr(f, 'free_symbols') else set()
    if free_syms:
        sym = list(free_syms)[0]
    else:
        sym = x

    # H_1: f is continuous on Reals
    h1_ok = False
    try:
        domain = continuous_domain(f, sym, sympy.S.Reals)
        if domain == sympy.S.Reals:
            h1_ok = True
    except Exception:
        pass

    # neg_Q: f is NOT uniformly continuous on Reals
    # A uniformly continuous function must satisfy limit(f(x + delta(x)) - f(x)) == 0
    # for any delta(x) -> 0 as x -> oo or x -> -oo.
    neg_q_ok = False
    try:
        # Test sequences delta(x) -> 0 as x -> oo
        deltas_pos = [
            1 / sym,
            1 / sympy.sqrt(sym),
            1 / sym**2,
            sympy.exp(-sym),
            1 / sympy.log(sym + 2),
            1 / sym**sympy.Rational(1, 3)
        ]
        for delta in deltas_pos:
            try:
                L = sympy.limit(f.subs(sym, sym + delta) - f, sym, sympy.oo)
                # If the limit is non-zero, or oscillates (AccumBounds), it's not uniformly continuous
                if L != 0 and not isinstance(L, sympy.Limit):
                    neg_q_ok = True
                    break
            except Exception:
                pass
        
        # Test sequences delta(x) -> 0 as x -> -oo
        if not neg_q_ok:
            deltas_neg = [
                1 / sym,
                1 / sympy.sqrt(-sym),
                1 / sym**2,
                sympy.exp(sym),
                1 / sympy.log(-sym + 2),
                1 / (-sym)**sympy.Rational(1, 3)
            ]
            for delta in deltas_neg:
                try:
                    L = sympy.limit(f.subs(sym, sym + delta) - f, sym, -sympy.oo)
                    if L != 0 and not isinstance(L, sympy.Limit):
                        neg_q_ok = True
                        break
                except Exception:
                    pass

        # Fallback for polynomials: any polynomial of degree >= 2 is not uniformly continuous on R
        if not neg_q_ok:
            try:
                if f.is_polynomial(sym):
                    deg = sympy.degree(f, sym)
                    if deg >= 2:
                        neg_q_ok = True
            except Exception:
                pass
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a continuous function on R",
    "¬Q: f is not uniformly continuous on R"
]

N_HYP = 1
NEG_Q_INDEX = 1