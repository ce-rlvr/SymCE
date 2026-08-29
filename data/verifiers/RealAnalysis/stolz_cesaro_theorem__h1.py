import sympy as sp

# Top-level setup
n = sp.Symbol('n', positive=True, integer=True)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two sympy expressions (a_n, b_n) or a dictionary
    with keys 'a' and 'b'.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
        elif isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
        else:
            return [False, False, False, False]
            
        if callable(a): a = a(n)
        if callable(b): b = b(n)
    except Exception:
        return [False, False, False, False]

    # H_1: (b_n) is strictly monotonically increasing
    h1 = False
    try:
        diff_b = sp.simplify(b.subs(n, n+1) - b)
        if diff_b.is_positive:
            h1 = True
        elif diff_b.is_positive is False:
            h1 = False
        else:
            is_inc = True
            for i in range(1, 50):
                v1 = float(b.subs(n, i).evalf())
                v2 = float(b.subs(n, i+1).evalf())
                if v2 <= v1:
                    is_inc = False
                    break
            h1 = is_inc
    except Exception:
        h1 = False

    # H_2: lim_{n -> oo} b_n = +oo
    h2 = False
    try:
        L_b = sp.limit(b, n, sp.oo)
        if L_b == sp.oo:
            h2 = True
        else:
            v1 = float(b.subs(n, 100).evalf())
            v2 = float(b.subs(n, 1000).evalf())
            if v2 > v1 and v2 > 100:
                h2 = True
    except Exception:
        h2 = False

    # H_3: lim_{n -> oo} (a_{n+1} - a_n) / (b_{n+1} - b_n) = L where L in R U {-oo, oo}
    h3 = False
    L = None
    try:
        diff_a = sp.simplify(a.subs(n, n+1) - a)
        diff_b = sp.simplify(b.subs(n, n+1) - b)
        diff_q = sp.simplify(diff_a / diff_b)
        L = sp.limit(diff_q, n, sp.oo)
        if not isinstance(L, sp.Limit):
            if L == sp.oo or L == -sp.oo or L.is_real:
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: lim_{n -> oo} a_n / b_n != L
    neg_q = False
    try:
        if h3 and L is not None:
            q = sp.simplify(a / b)
            L_q = sp.limit(q, n, sp.oo)
            if isinstance(L_q, sp.Limit):
                try:
                    v_large = complex(q.subs(n, 10000).evalf())
                    if L == sp.oo:
                        neg_q = (abs(v_large) < 1000)
                    elif L == -sp.oo:
                        neg_q = (v_large.real > -1000)
                    else:
                        neg_q = (abs(v_large - complex(L)) > 0.1)
                except Exception:
                    neg_q = True
            else:
                neg_q = bool(L_q != L)
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (b_n) is strictly monotonically increasing",
    "H_2: lim_{n -> oo} b_n = +oo",
    "H_3: lim_{n -> oo} (a_{n+1} - a_n) / (b_{n+1} - b_n) = L where L in R U {-oo, oo}",
    "¬Q: lim_{n -> oo} a_n / b_n != L"
]

N_HYP = 3
NEG_Q_INDEX = 3