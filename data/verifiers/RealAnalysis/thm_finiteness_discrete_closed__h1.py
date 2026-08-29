import sympy
from sympy import S, FiniteSet, Union, ImageSet, Lambda, Symbol, diff

# Top-level setup for potential witness expressions
x = Symbol('x')
n = Symbol('n')

def is_discrete_closed(D):
    """Helper to check if a sympy set is discrete and closed in R."""
    try:
        if hasattr(D, 'is_subset') and D.is_subset(S.Integers) == True:
            return True
        if isinstance(D, FiniteSet):
            return True
        if isinstance(D, Union):
            return all(is_discrete_closed(arg) for arg in D.args)
        if hasattr(D, 'base_set') and hasattr(D, 'lamda'):
            if D.base_set in (S.Integers, S.Naturals, S.Naturals0):
                expr = D.lamda.expr
                var = D.lamda.variables[0]
                deriv = diff(expr, var)
                if deriv.is_constant() and deriv != 0:
                    return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # Unpack witness. It can be a tuple (D, K) or just D (with K implicitly R)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            D, K = witness
        else:
            D = witness
            K = S.Reals
    except Exception:
        D = witness
        K = S.Reals

    # H_1: D is a subset of K
    try:
        h1 = False
        if hasattr(D, 'is_subset') and D.is_subset(K) == True:
            h1 = True
        elif K == S.Reals and hasattr(D, 'is_subset') and D.is_subset(S.Reals) == True:
            h1 = True
    except Exception:
        h1 = False

    # H_2: D is closed in R^n
    try:
        h2 = False
        if is_discrete_closed(D):
            h2 = True
        else:
            if hasattr(D, 'is_closed'):
                closed = D.is_closed
                if closed is True:
                    h2 = True
                elif closed is None:
                    if hasattr(D, 'closure') and D.closure == D:
                        h2 = True
    except Exception:
        h2 = False

    # H_3: Every point in D is an isolated point of D
    try:
        h3 = False
        if is_discrete_closed(D):
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: The set D contains only a finite number of elements (Negation: D is infinite)
    try:
        neg_q = False
        if hasattr(D, 'is_finite') and D.is_finite == False:
            neg_q = True
        elif D in (S.Integers, S.Naturals, S.Naturals0, S.Reals):
            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: D is a subset of K",
    "H_2: D is closed in R^n",
    "H_3: Every point in D is an isolated point of D",
    "¬Q: D is not finite"
]

N_HYP = 3
NEG_Q_INDEX = 3