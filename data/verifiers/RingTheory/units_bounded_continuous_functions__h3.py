import sympy
from sympy import Symbol, Abs, S
from sympy.calculus.util import continuous_domain, function_range

x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The witness can be a sympy expression `f` (with implicit domain S.Reals),
    or a tuple `(f, X_space)` where `X_space` is a sympy Set.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, X_space = witness
        else:
            f = witness
            X_space = S.Reals
    except Exception:
        return [False, False, False]

    # H_1: X is a topological space
    try:
        h1 = isinstance(X_space, sympy.Set)
    except Exception:
        h1 = False

    # H_2: C_b(X, R) is the ring of bounded continuous real-valued functions on X
    h2 = True

    # ¬Q: The conclusion fails at the witness
    try:
        if not isinstance(f, sympy.Expr):
            f = sympy.sympify(f)

        syms = f.free_symbols
        if syms:
            sym = list(syms)[0]
        else:
            sym = x

        # Check if f is in C_b(X, R)
        cd = continuous_domain(f, sym, S.Reals)
        is_continuous = X_space.is_subset(cd)

        fr = function_range(f, sym, X_space)
        is_bounded = fr.is_bounded

        in_Cb = is_continuous and is_bounded

        # Check if f is a unit in C_b(X, R)
        if in_Cb:
            cd_inv = continuous_domain(1/f, sym, S.Reals)
            is_continuous_inv = X_space.is_subset(cd_inv)
            fr_inv = function_range(1/f, sym, X_space)
            is_bounded_inv = fr_inv.is_bounded
            is_unit = is_continuous_inv and is_bounded_inv
        else:
            is_unit = False

        # Check if there exists epsilon > 0 such that |f(x)| >= epsilon for all x in X
        abs_f = Abs(f)
        fr_abs = function_range(abs_f, sym, X_space)
        inf_abs = fr_abs.inf

        has_epsilon = bool(inf_abs > 0)

        # The conjecture claims: is_unit <==> has_epsilon
        # The negation is that they are not equivalent
        neg_q = bool(is_unit != has_epsilon)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: C_b(X, R) is the ring of bounded continuous real-valued functions on X under pointwise operations",
    "¬Q: f is a unit in C_b(X, R) is not equivalent to there exists epsilon > 0 such that |f(x)| >= epsilon for all x in X"
]

N_HYP = 2
NEG_Q_INDEX = 2