import sympy
from sympy import Symbol, Sum, oo, limit

n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two SymPy expressions in terms of n: (a_n, b_n).
    """
    try:
        a_n, b_n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: (a_n) and (b_n) are sequences of real numbers
    try:
        h1 = True
        for i in range(1, 11):
            v_a = complex(a_n.subs(n, i).evalf())
            v_b = complex(b_n.subs(n, i).evalf())
            if abs(v_a.imag) > 1e-12 or abs(v_b.imag) > 1e-12:
                h1 = False
                break
    except Exception:
        h1 = False

    # H_2: The series sum_{n=1}^infty a_n converges to a finite real number
    try:
        s = Sum(a_n, (n, 1, oo))
        conv = s.is_convergent()
        if conv is True:
            h2 = True
        elif conv is False:
            h2 = False
        else:
            val = s.doit()
            if val.has(oo, -oo, sympy.zoo, sympy.nan):
                h2 = False
            elif val.is_number:
                try:
                    cval = complex(val.evalf())
                    h2 = True
                except Exception:
                    h2 = False
            else:
                h2 = False
    except Exception:
        h2 = False

    # H_3: (b_n) is a monotonic sequence
    try:
        diff = sympy.simplify(b_n.subs(n, n+1) - b_n)
        if diff.is_nonnegative is True or diff.is_nonpositive is True:
            h3 = True
        else:
            is_inc = True
            is_dec = True
            for i in range(1, 101):
                val = float(diff.subs(n, i).evalf())
                if val < -1e-12:
                    is_inc = False
                if val > 1e-12:
                    is_dec = False
            h3 = is_inc or is_dec
    except Exception:
        h3 = False

    # ¬Q: The series sum_{n=1}^infty a_n b_n diverges
    try:
        s_ab = Sum(a_n * b_n, (n, 1, oo))
        conv_ab = s_ab.is_convergent()
        if conv_ab is False:
            neg_q = True
        elif conv_ab is True:
            neg_q = False
        else:
            val_ab = s_ab.doit()
            if val_ab.has(oo, -oo, sympy.zoo, sympy.nan):
                neg_q = True
            elif val_ab.is_number:
                try:
                    cval = complex(val_ab.evalf())
                    neg_q = False
                except Exception:
                    neg_q = True
            else:
                term_limit = limit(a_n * b_n, n, oo)
                if term_limit != 0:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (a_n) and (b_n) are sequences of real numbers",
    "H_2: The series sum_{n=1}^infty a_n converges to a finite real number",
    "H_3: (b_n) is a monotonic sequence",
    "¬Q: The series sum_{n=1}^infty a_n b_n diverges"
]

N_HYP = 3
NEG_Q_INDEX = 3