import sympy
from sympy import Symbol, Interval, integrate, diff, solveset, S
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        f, alpha, a, b = witness
        f = sympy.sympify(f)
        alpha = sympy.sympify(alpha)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False]
        
    try:
        if float(a) >= float(b):
            h1 = False
        else:
            domain = continuous_domain(f, x, Interval(a, b))
            h1 = bool(domain == Interval(a, b))
    except Exception:
        h1 = False
        
    try:
        integrand = f * diff(alpha, x)
        I = integrate(integrand, (x, a, b))
        if I.has(sympy.Integral):
            neg_q = False
        else:
            rhs = alpha.subs(x, b) - alpha.subs(x, a)
            eq = sympy.simplify(f * rhs - I)
            
            if eq.is_constant():
                neg_q = bool(eq != 0)
            else:
                sols = solveset(eq, x, domain=Interval(a, b))
                if sols == S.EmptySet:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuous on the interval",
    "¬Q: There is no c in the interval such that the integral equals f(c)(alpha(b) - alpha(a))"
]

N_HYP = 1
NEG_Q_INDEX = 1