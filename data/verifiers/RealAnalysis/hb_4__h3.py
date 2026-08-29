import sympy

k = sympy.Symbol('k', integer=True, positive=True)

def conditions(witness):
    """
    witness is expected to be a dictionary with:
      'S': a sympy Set representing the subset of R
      'x': a sympy Expr representing the sequence x_k in terms of k
    Alternatively, a tuple (S, x) is accepted.
    """
    try:
        if isinstance(witness, dict):
            S_set = witness['S']
            x_expr = witness['x']
        else:
            S_set, x_expr = witness
    except Exception:
        return [False, False, False, False]

    # H_1: S is a subset of R^n (we restrict to R for simplicity in verification)
    try:
        h1 = (S_set.is_subset(sympy.S.Reals) == True)
    except Exception:
        h1 = False

    # H_2: S is closed
    try:
        h2 = (S_set.closure == S_set)
    except Exception:
        h2 = False

    # H_3: (x_k) is a sequence of points in S
    try:
        h3 = True
        # Check the first 100 terms to verify the sequence is in S
        for i in range(1, 101):
            val = x_expr.subs(k, i)
            if S_set.contains(val) != True:
                h3 = False
                break
    except Exception:
        h3 = False

    # ¬Q: (x_k) has no subsequence that converges to a limit point L in S.
    # Since S is closed (if H_2 holds), any convergent subsequence in R would converge to a point in S.
    # Thus, the sequence must have NO convergent subsequence in R at all.
    # By the Bolzano-Weierstrass theorem, this is equivalent to the sequence being unbounded.
    try:
        lim = sympy.limit(sympy.Abs(x_expr), k, sympy.oo)
        neg_q = (lim == sympy.oo)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is a subset of R",
    "H_2: S is closed",
    "H_3: (x_k) is a sequence of points in S",
    "¬Q: (x_k) has no subsequence that converges to a limit point in S"
]

N_HYP = 3
NEG_Q_INDEX = 3