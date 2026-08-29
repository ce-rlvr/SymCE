import sympy
from sympy import Symbol, S, Interval, oo
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup for witness expressions
x = Symbol('x', real=True)
R = S.Reals

CONDITION_LABELS = [
    "H_1: F is an equicontinuous family of real-valued functions on X",
    "H_2: There exists x0 in X such that {f(x0) : f in F} is bounded",
    "¬Q: The family F is NOT uniformly bounded on X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness tuple (domain, F, x0) where:
      - domain is a sympy Set (e.g., S.Reals)
      - F is a list of sympy expressions in terms of x
      - x0 is a point in the domain
    Checks if it is a valid counterexample.
    """
    try:
        domain, F, x0 = witness
    except Exception:
        return [False, False, False]
    
    if not isinstance(F, (list, tuple)):
        F = [F]
        
    # H_1: F is an equicontinuous family on domain
    # For a finite family, equicontinuity is equivalent to each function being continuous on the domain.
    try:
        h1 = True
        if len(F) == 0:
            h1 = False
        else:
            for f in F:
                cd = continuous_domain(f, x, S.Reals)
                if not domain.is_subset(cd):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: There exists x0 in domain such that {f(x0) : f in F} is bounded
    try:
        h2 = False
        if sympy.sympify(domain.contains(x0)) == True:
            vals = [sympy.sympify(f).subs(x, x0) for f in F]
            if all(v.is_real and v.is_finite for v in vals):
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: F is NOT uniformly bounded on domain
    try:
        is_unif_bounded = True
        for f in F:
            fr = function_range(f, x, domain)
            if not (fr.inf.is_finite and fr.sup.is_finite):
                is_unif_bounded = False
                break
        neg_q = not is_unif_bounded
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]