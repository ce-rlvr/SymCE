import sympy as sp
from sympy.ntheory import continued_fraction_iterator

def conditions(witness):
    try:
        x, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: x is a real number with simple continued fraction expansion
    try:
        h1 = False
        if isinstance(x, (int, float)):
            h1 = True
        else:
            x_sym = sp.sympify(x)
            if x_sym.is_real:
                h1 = True
        
        if h1:
            if isinstance(x, float):
                x_val = sp.Rational(str(x))
            else:
                x_val = sp.sympify(x)
            it = continued_fraction_iterator(x_val)
            next(it)  # Must have at least one term
    except Exception:
        h1 = False

    # H_2: n >= 2 is an integer
    try:
        h2 = isinstance(n, int) and n >= 2
    except Exception:
        h2 = False

    # ¬Q: p_n q_{n-2} - p_{n-2} q_n != (-1)^n a_n
    try:
        if isinstance(x, float):
            x_val = sp.Rational(str(x))
        else:
            x_val = sp.sympify(x)
            
        if not getattr(x_val, 'is_real', True):
            neg_q = False
        elif not isinstance(n, int) or n < 2:
            neg_q = False
        else:
            it = continued_fraction_iterator(x_val)
            a = []
            for _ in range(n + 1):
                try:
                    a.append(next(it))
                except StopIteration:
                    break
            
            # If the continued fraction terminates before index n, a_n is undefined,
            # so the conclusion equation fails to hold.
            if len(a) <= n:
                neg_q = True
            else:
                a_n = a[n]
                p = []
                q = []
                for i in range(n + 1):
                    if i == 0:
                        p.append(a[0])
                        q.append(1)
                    elif i == 1:
                        p.append(a[1]*a[0] + 1)
                        q.append(a[1])
                    else:
                        p.append(a[i]*p[i-1] + p[i-2])
                        q.append(a[i]*q[i-1] + q[i-2])
                
                lhs = p[n] * q[n-2] - p[n-2] * q[n]
                rhs = ((-1)**n) * a_n
                neg_q = bool(sp.simplify(lhs - rhs) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is a real number with simple continued fraction expansion",
    "H_2: n >= 2 is an integer",
    "not Q: p_n q_{n-2} - p_{n-2} q_n != (-1)^n a_n"
]

N_HYP = 2
NEG_Q_INDEX = 2