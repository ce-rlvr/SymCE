import sympy
from sympy import Symbol, Interval, solveset, integrate, EmptySet, Union, FiniteSet, Intersection, Complement

x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is a non-negative continuous function defined on a to b",
    "H_2: S is the set of all x in a to b such that f(x) >= c",
    "H_3: S is a finite union of intervals with total length L",
    "¬Q: L > (1/c) * integral f(x)dx or is undefined"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        f, a, b, c = witness
    except Exception:
        return [False, False, False, False]
    
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        c = sympy.sympify(c)
        
        if not (a.is_number and b.is_number and c.is_number):
            return [False, False, False, False]
            
        if isinstance(f, str):
            f = sympy.sympify(f, locals={'x': x})
        else:
            f = sympy.sympify(f)
            free_xs = [s for s in f.free_symbols if s.name == 'x']
            for free_x in free_xs:
                f = f.subs(free_x, x)
                
        if a.is_real and b.is_real and bool(a < b):
            domain = Interval(a, b)
            
            # Check non-negativity
            neg_set = solveset(f < 0, x, domain=domain)
            is_non_negative = False
            if neg_set == EmptySet:
                is_non_negative = True
            elif isinstance(neg_set, sympy.ConditionSet):
                is_non_negative = True
                for i in range(101):
                    val = f.subs(x, a + (b - a) * i / 100)
                    if val.is_real and val < 0:
                        is_non_negative = False
                        break
            else:
                is_non_negative = False
                
            # Check continuity
            is_continuous = False
            if f.is_polynomial(x) or f.is_constant():
                is_continuous = True
            else:
                is_continuous = True
                for i in range(101):
                    val = f.subs(x, a + (b - a) * i / 100)
                    if not val.is_real or val.has(sympy.oo, sympy.zoo, sympy.nan, -sympy.oo):
                        is_continuous = False
                        break
                        
            if is_non_negative and is_continuous:
                h1 = True
    except Exception:
        h1 = False

    try:
        if h1:
            domain = Interval(a, b)
            S_set = solveset(f >= c, x, domain=domain)
            h2 = True
    except Exception:
        h2 = False

    try:
        if h2:
            if isinstance(S_set, (Interval, Union, FiniteSet, EmptySet, Intersection, Complement)):
                L = S_set.measure
                h3 = True
    except Exception:
        h3 = False

    try:
        if h3:
            if c <= 0:
                neg_q = True
            else:
                integral_val = integrate(f, (x, a, b))
                rhs = (1 / c) * integral_val
                if bool(L > rhs):
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]