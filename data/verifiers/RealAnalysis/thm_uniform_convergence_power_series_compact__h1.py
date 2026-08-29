import sympy
from sympy import limit, oo, Abs, Interval, Symbol, Sum, Max

CONDITION_LABELS = [
    "H_1: The power series has a radius of convergence R > 0",
    "H_2: K is a compact subset of the open interval (-R, R)",
    "¬Q: The power series does not converge uniformly on K"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a_n = sympy.sympify(witness['a_n'])
            R = sympy.sympify(witness['R'])
            K = witness['K']
            n = witness.get('n', Symbol('n'))
        else:
            if len(witness) == 4:
                a_n, n, R, K = witness
                a_n = sympy.sympify(a_n)
                R = sympy.sympify(R)
            elif len(witness) == 3:
                a_n, R, K = witness
                a_n = sympy.sympify(a_n)
                R = sympy.sympify(R)
                free = a_n.free_symbols
                if len(free) == 1:
                    n = list(free)[0]
                else:
                    n = Symbol('n')
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    def is_equal(r1, r2):
        if r1 is None or r2 is None:
            return False
        if r1 == r2:
            return True
        try:
            if abs(float(r1) - float(r2)) < 1e-9:
                return True
        except Exception:
            pass
        try:
            if sympy.simplify(r1 - r2) == 0:
                return True
        except Exception:
            pass
        return False

    # H1: The power series has a radius of convergence R > 0.
    h1 = False
    try:
        if float(R) > 0:
            R_actual = None
            try:
                L = limit(Abs(a_n.subs(n, n+1) / a_n), n, oo)
                if not L.has(sympy.Limit):
                    if L == 0:
                        R_actual = oo
                    elif L == oo:
                        R_actual = 0
                    else:
                        R_actual = 1 / L
            except Exception:
                pass
            
            if not is_equal(R_actual, R):
                try:
                    L2 = limit(Abs(a_n)**(1/n), n, oo)
                    if not L2.has(sympy.Limit):
                        if L2 == 0:
                            R_actual = oo
                        elif L2 == oo:
                            R_actual = 0
                        else:
                            R_actual = 1 / L2
                except Exception:
                    pass
            
            if is_equal(R_actual, R):
                h1 = True
    except Exception:
        h1 = False

    # H2: K is a compact subset of the open interval (-R, R).
    h2 = False
    try:
        if K.is_subset(Interval.open(-R, R)):
            if K.is_closed and K.is_bounded:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The power series does NOT converge uniformly on K.
    neg_q = False
    try:
        if K.is_EmptySet:
            neg_q = False
        else:
            inf_K = K.inf
            sup_K = K.sup
            r = Max(Abs(inf_K), Abs(sup_K))
            
            r_val = float(r)
            R_val = float(R)
            
            if r_val < R_val:
                neg_q = False
            elif r_val > R_val:
                neg_q = True
            else:
                if r_val == float(oo):
                    if a_n.subs(n, 1000) == 0:
                        neg_q = False
                    else:
                        neg_q = True
                else:
                    diverges_at_boundary = False
                    for pt in [inf_K, sup_K]:
                        if abs(float(pt)) == R_val and K.contains(pt) == True:
                            term = a_n * (pt ** n)
                            start_n = 0
                            for i in range(10):
                                try:
                                    val = term.subs(n, i)
                                    if not val.has(sympy.oo, sympy.nan, sympy.zoo) and val.is_finite is not False:
                                        start_n = i
                                        break
                                except Exception:
                                    pass
                            s = Sum(term, (n, start_n, oo))
                            conv = s.is_convergent()
                            if conv is False:
                                diverges_at_boundary = True
                                break
                    if diverges_at_boundary:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]