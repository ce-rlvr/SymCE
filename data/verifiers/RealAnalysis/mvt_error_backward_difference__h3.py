import sympy
from sympy import Symbol, Interval, EmptySet
from sympy.calculus.util import continuous_domain

t = Symbol('t', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (f, x_val, h_val)
    where f is a sympy expression in t, and x_val, h_val are real numbers.
    """
    try:
        f, x_val, h_val = witness
    except Exception:
        return [False, False, False]
        
    try:
        f1 = sympy.diff(f, t)
        f2 = sympy.diff(f1, t)
    except Exception:
        return [False, False, False]
        
    # H_1: f is twice differentiable on [x-h, x]
    try:
        iv = Interval(x_val - h_val, x_val)
        dom_f = continuous_domain(f, t, iv)
        dom_f1 = continuous_domain(f1, t, iv)
        dom_f2 = continuous_domain(f2, t, iv)
        h1_ok = bool(iv.is_subset(dom_f) and iv.is_subset(dom_f1) and iv.is_subset(dom_f2))
    except Exception:
        h1_ok = False
        
    # H_2: f'' is continuous on [x-h, x]
    try:
        iv = Interval(x_val - h_val, x_val)
        dom_f2 = continuous_domain(f2, t, iv)
        h2_ok = bool(iv.is_subset(dom_f2))
    except Exception:
        h2_ok = False
        
    # ¬Q: There does not exist c in (x-h, x) such that f'(x) - (f(x) - f(x-h))/h = (h/2)f''(c)
    try:
        if h_val <= 0:
            neg_q = True
        else:
            lhs = f1.subs(t, x_val) - (f.subs(t, x_val) - f.subs(t, x_val - h_val)) / h_val
            c = Symbol('c', real=True)
            rhs = (h_val / 2) * f2.subs(t, c)
            eq = sympy.Eq(lhs, rhs)
            sols = sympy.solveset(eq, c, domain=Interval.open(x_val - h_val, x_val))
            
            if sols == EmptySet:
                neg_q = True
            elif isinstance(sols, sympy.Set) and sols.is_empty == False:
                neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is twice differentiable on interval",
    "H_2: f double prime is continuous on interval",
    "not_Q: conclusion fails"
]

N_HYP = 2
NEG_Q_INDEX = 2