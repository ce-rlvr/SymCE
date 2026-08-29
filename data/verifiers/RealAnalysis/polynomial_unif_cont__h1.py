import sympy
from sympy import Symbol, sin, cos, exp, pi, oo, S, degree, diff
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        witness = sympy.sympify(witness)
    except Exception:
        return [False]

    try:
        free_syms = witness.free_symbols
        if free_syms:
            v = list(free_syms)[0]
        else:
            v = x
    except Exception:
        v = x

    # Check if the witness is uniformly continuous on R
    is_uc = False
    try:
        if continuous_domain(witness, v, S.Reals) != S.Reals:
            is_uc = False
        elif witness.is_polynomial(v) == True:
            is_uc = bool(degree(witness, v) <= 1)
        else:
            dP = diff(witness, v)
            try:
                fr = function_range(dP, v, S.Reals)
                if fr.inf > -oo and fr.sup < oo:
                    is_uc = True
                else:
                    raise ValueError("Check outside compact set")
            except Exception:
                try:
                    # If global range fails or is unbounded, check if derivative is bounded outside [-1, 1]
                    # (A continuous function on R with bounded derivative outside a compact set is uniformly continuous)
                    fr_plus = function_range(dP, v, sympy.Interval(1, oo))
                    fr_minus = function_range(dP, v, sympy.Interval(-oo, -1))
                    if fr_plus.inf > -oo and fr_plus.sup < oo and fr_minus.inf > -oo and fr_minus.sup < oo:
                        is_uc = True
                    else:
                        is_uc = False
                except Exception:
                    is_uc = False
    except Exception:
        # Fallbacks for common counterexamples if calculus utilities fail
        try:
            if witness == sympy.sin(v) or witness == sympy.cos(v) or witness == abs(v):
                is_uc = True
            else:
                is_uc = False
        except Exception:
            is_uc = False

    # Check if the degree of the witness is <= 1
    deg_le_1 = False
    try:
        if witness.is_polynomial(v) == True:
            deg_le_1 = bool(degree(witness, v) <= 1)
        else:
            deg_le_1 = False
    except Exception:
        deg_le_1 = False

    # Evaluate the conclusion: P is uniformly continuous on R iff degree of P <= 1
    try:
        Q = (is_uc == deg_le_1)
        neg_Q = not Q
    except Exception:
        neg_Q = False
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: It is NOT true that (P is uniformly continuous on R iff degree of P <= 1)"
]

N_HYP = 0
NEG_Q_INDEX = 0