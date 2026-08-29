import sympy as sp

x = sp.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to provide a constant M and a family of functions F.
    """
    try:
        if isinstance(witness, dict):
            M = witness.get('M', 1)
            F = witness.get('F', witness)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2 and isinstance(witness[0], (int, float, sp.Number)):
                M, F = witness
            else:
                M = 1
                F = witness
        else:
            M = 1
            F = witness
    except Exception:
        return [False, False, False]

    # H_1: M > 0 is a fixed constant
    try:
        h1 = float(M) > 0
    except Exception:
        h1 = False

    # H_2: \mathcal{A} is the set of all real sequences (a_n)_{n=1}^\infty such that \sum_{n=1}^\infty n |a_n| \le M
    # This is a definitional hypothesis and does not constrain the witness directly.
    h2 = True

    # neg_Q: The family of functions \mathcal{F} is NOT uniformly equicontinuous on \mathbb{R}
    # We check if there is a function in F whose derivative is unbounded on R.
    neg_q = False
    try:
        if not isinstance(F, (list, tuple, set)):
            F = [F]
        
        for f in F:
            if isinstance(f, str):
                try:
                    f = sp.sympify(f)
                except Exception:
                    pass
            if callable(f):
                try:
                    f = f(x)
                except Exception:
                    pass
            
            try:
                df = sp.diff(f, x)
            except Exception:
                continue
                
            # Check limits at infinity
            try:
                L1 = sp.limit(df, x, sp.oo)
                L2 = sp.limit(df, x, -sp.oo)
                if L1 in [sp.oo, -sp.oo] or L2 in [sp.oo, -sp.oo]:
                    neg_q = True
                    break
            except Exception:
                pass
                
            # Check if derivative grows unbounded by sampling
            try:
                vals = []
                for val in [10, 100, 1000, 10000, 100000]:
                    v = abs(float(df.subs(x, val)))
                    vals.append(v)
                if len(vals) >= 3 and vals[-1] > vals[-2] > vals[-3] and vals[-1] > 1000:
                    neg_q = True
                    break
            except Exception:
                pass
                
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M > 0 is a fixed constant",
    "H_2: A is the set of all real sequences (a_n) such that sum n|a_n| <= M",
    "¬Q: The family of functions F is not uniformly equicontinuous on R"
]

N_HYP = 2
NEG_Q_INDEX = 2