import sympy
from sympy import Symbol, S, diff, Union, Interval, FiniteSet
from sympy.calculus.util import continuous_domain, function_range

x = Symbol('x', real=True)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        f, I = witness
    except Exception:
        return [False, False]

    # H_1: f is a differentiable function on I
    try:
        f_prime = diff(f, x)
        dom_f = continuous_domain(f, x, S.Reals)
        dom_f_prime = continuous_domain(f_prime, x, S.Reals)
        h1_val = I.is_subset(dom_f) and I.is_subset(dom_f_prime)
        h1 = (h1_val == True)
    except Exception:
        h1 = False

    # neg_Q: f'(I) is not a connected subset of ℝ
    try:
        def image_of_set(g, domain):
            if domain == S.EmptySet:
                return S.EmptySet
            elif isinstance(domain, Union):
                ranges = [image_of_set(g, arg) for arg in domain.args]
                return Union(*ranges)
            elif isinstance(domain, FiniteSet):
                return FiniteSet(*[g.subs(x, val) for val in domain])
            elif isinstance(domain, Interval):
                return function_range(g, x, domain)
            else:
                return function_range(g, x, domain)

        f_prime_image = image_of_set(f_prime, I)

        def is_connected(s):
            if s in (S.Reals, S.EmptySet):
                return True
            if isinstance(s, Interval):
                return True
            if isinstance(s, FiniteSet) and len(s) <= 1:
                return True
            return False

        neg_q = not is_connected(f_prime_image)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a differentiable function on I",
    "¬Q: f'(I) is not a connected subset of ℝ"
]

N_HYP = 1
NEG_Q_INDEX = 1