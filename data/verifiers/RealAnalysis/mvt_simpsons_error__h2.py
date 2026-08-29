import sympy
from sympy import Symbol, Interval, EmptySet, simplify, integrate, Rational

x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is 4 times continuously differentiable on the closed interval a to b",
    "¬Q: No c in the open interval a to b satisfies the error formula"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        f, a, b = witness
        if callable(f):
            f = f(x)
        f = sympy.sympify(f)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        
        if not (a.is_real and b.is_real):
            return [False, False]
    except Exception:
        return [False, False]
    
    h1_ok = False
    try:
        if a > b:
            interval = EmptySet
        else:
            interval = Interval(a, b)
            
        f4 = f.diff(x, 4)
        if f4.is_polynomial(x):
            h1_ok = True
        else:
            sings = sympy.singularities(f4, x)
            if interval.intersect(sings) == sympy.EmptySet:
                h1_ok = True
    except Exception:
        h1_ok = False
        
    neg_q_ok = False
    try:
        if a >= b:
            neg_q_ok = True
        else:
            integral_val = integrate(f, (x, a, b))
            mid = (a + b) / 2
            simpson_val = (b - a) / 6 * (f.subs(x, a) + 4 * f.subs(x, mid) + f.subs(x, b))
            E = simplify(integral_val - simpson_val)
            K = Rational(-1, 2880) * (b - a)**5
            
            if K == 0:
                if E != 0:
                    neg_q_ok = True
                else:
                    neg_q_ok = False
            else:
                target_f4 = simplify(E / K)
                diff_eq = simplify(f4 - target_f4)
                if diff_eq.is_constant() and diff_eq != 0:
                    neg_q_ok = True
                else:
                    sols = sympy.solveset(diff_eq, x, domain=Interval.open(a, b))
                    if sols is sympy.EmptySet:
                        neg_q_ok = True
                    else:
                        neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]