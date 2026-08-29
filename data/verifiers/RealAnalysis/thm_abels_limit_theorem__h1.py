import sympy as sp

n = sp.Symbol('n', integer=True, positive=True)
x = sp.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            a_n, R = witness
            if callable(a_n):
                a_n = a_n(n)
            a_n = sp.sympify(a_n)
            R = sp.sympify(R)
            
            try:
                root = sp.limit(sp.Abs(a_n)**(1/n), n, sp.oo)
                if root == 0:
                    R_actual = sp.oo
                else:
                    R_actual = 1 / root
            except Exception:
                try:
                    ratio = sp.Abs(a_n / a_n.subs(n, n + 1))
                    R_actual = sp.limit(ratio, n, sp.oo)
                except Exception:
                    R_actual = None
            
            if R_actual is not None:
                if sp.simplify(R - R_actual) != 0:
                    return [False, False, False]
        else:
            a_n = witness
            if callable(a_n):
                a_n = a_n(n)
            a_n = sp.sympify(a_n)
            try:
                root = sp.limit(sp.Abs(a_n)**(1/n), n, sp.oo)
                if root == 0:
                    R = sp.oo
                else:
                    R = 1 / root
            except Exception:
                try:
                    ratio = sp.Abs(a_n / a_n.subs(n, n + 1))
                    R = sp.limit(ratio, n, sp.oo)
                except Exception:
                    R = None
    except Exception:
        return [False, False, False]

    try:
        if a_n.has(x):
            return [False, False, False]
    except Exception:
        pass

    try:
        if R is not None and R.is_real and R > 0 and R < sp.oo:
            H1 = True
        else:
            H1 = False
    except Exception:
        H1 = False

    try:
        if H1:
            term = a_n * (R**n)
            conv = sp.Sum(term, (n, 1, sp.oo)).is_convergent()
            H2 = (conv is True)
        else:
            H2 = False
    except Exception:
        H2 = False

    try:
        if H1:
            term = a_n * (R**n)
            conv = sp.Sum(term, (n, 1, sp.oo)).is_convergent()
            if conv is True:
                neg_Q = False
            elif conv is False:
                neg_Q = True
            else:
                neg_Q = False
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [bool(H1), bool(H2), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: The power series has a finite radius of convergence R > 0",
    "H_2: The series sum a_n R^n converges",
    "¬Q: The power series does not converge uniformly on the closed interval from 0 to R"
]

N_HYP = 2
NEG_Q_INDEX = 2