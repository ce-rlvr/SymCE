import sympy
from sympy import Symbol, Interval, Union, EmptySet, Set
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup
x = Symbol('x', real=True)

def is_open_set(S):
    if not isinstance(S, Set):
        return False
    try:
        if S.is_open is True:
            return True
    except Exception:
        pass
    try:
        if S.interior == S:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        f, a, b, U, V = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: f is a continuous function from the interval to R
    try:
        f = sympy.sympify(f)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        if not (a.is_real and b.is_real and bool(a < b)):
            h1 = False
        else:
            domain = Interval(a, b)
            cd = continuous_domain(f, x, domain)
            h1 = (cd == domain)
    except Exception:
        h1 = False

    # H2: U and V are disjoint open subsets of R
    try:
        if is_open_set(U) and is_open_set(V):
            disjoint = (U.intersect(V) == EmptySet)
            h2 = bool(disjoint)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: image of f intersection U is not empty
    try:
        domain = Interval(a, b)
        image = function_range(f, x, domain)
        h3 = bool(image.intersect(U) != EmptySet)
    except Exception:
        h3 = False

    # neg_Q: image of f intersection V is not empty
    try:
        domain = Interval(a, b)
        image = function_range(f, x, domain)
        neg_q = bool(image.intersect(V) != EmptySet)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuous function from the interval to R",
    "H_2: U and V are disjoint open subsets of R",
    "H_3: image of f intersection U is not empty",
    "not Q: image of f intersection V is not empty"
]

N_HYP = 3
NEG_Q_INDEX = 3