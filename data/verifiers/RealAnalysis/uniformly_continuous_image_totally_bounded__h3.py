import sympy
from sympy import Symbol, S, Interval, oo
from sympy.calculus.util import maximum, minimum

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
Reals = S.Reals

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "H_2: f: X \\to Y is a uniformly continuous function",
    "¬Q: The image f(A) is not a totally bounded subset of Y"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness can be:
      - A dictionary with keys 'f' (sympy expression), 'A' (sympy Set), and optionally 'domain' (sympy Set).
      - A tuple (f, A) or (f, A, domain).
      - A single sympy expression f (in which case A and domain default to Reals).
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f', x)
            A = witness.get('A', S.Reals)
            domain = witness.get('domain', S.Reals)
        elif isinstance(witness, (tuple, list)):
            f = witness[0]
            A = witness[1] if len(witness) > 1 else S.Reals
            domain = witness[2] if len(witness) > 2 else S.Reals
        elif isinstance(witness, sympy.Expr):
            f = witness
            A = S.Reals
            domain = S.Reals
        else:
            return [False, False, False]

        # H_1: (X, d_X) and (Y, d_Y) are metric spaces
        # We assume X and Y are subsets of R with the standard metric.
        # We verify that A and domain are valid sets and A is a subset of the domain X.
        try:
            h1 = isinstance(A, sympy.Set) and isinstance(domain, sympy.Set) and bool(A.is_subset(domain))
        except Exception:
            h1 = False

        # H_2: f: X \to Y is a uniformly continuous function
        # We check if f has a bounded derivative on the domain (Lipschitz continuity is sufficient for uniform continuity).
        try:
            df = sympy.diff(f, x)
            if df.is_constant():
                h2 = True
            else:
                sup_df = maximum(abs(df), x, domain)
                h2 = bool(sup_df < oo)
        except Exception:
            h2 = False

        # ¬Q: The image f(A) is not a totally bounded subset of Y
        # In R, a set is totally bounded iff it is bounded. We check if f(A) is unbounded.
        try:
            sup_f = maximum(f, x, A)
            inf_f = minimum(f, x, A)
            neg_q = (sup_f == oo) or (inf_f == -oo)
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]