import sympy
from sympy import S, ImageSet, Union, ConditionSet, limit, Abs, oo

# Top-level setup for potential witness expressions
Z = S.Integers
N = S.Naturals
N0 = S.Naturals0
R = S.Reals
Q = S.Rationals

def has_no_accumulation_points(witness):
    """
    Helper function to determine if a set has no accumulation points in R.
    Returns True if we can definitively prove it has no accumulation points.
    """
    if witness in (S.Integers, S.Naturals, S.Naturals0):
        return True
        
    try:
        if witness.is_subset(S.Integers):
            return True
    except Exception:
        pass
        
    if isinstance(witness, ConditionSet):
        try:
            if witness.base_set.is_subset(S.Integers):
                return True
        except Exception:
            pass
            
    if isinstance(witness, Union):
        try:
            return all(has_no_accumulation_points(arg) for arg in witness.args)
        except Exception:
            return False
            
    if isinstance(witness, ImageSet):
        try:
            base = witness.base_sets[0]
            if base.is_subset(S.Integers):
                lam = witness.lamda
                if len(lam.variables) == 1:
                    expr = lam.expr
                    var = lam.variables[0]
                    
                    # Check if the sequence diverges to infinity as the variable goes to +oo
                    lim_pos_ok = True
                    if getattr(base, 'sup', None) == oo:
                        L = limit(Abs(expr), var, oo)
                        if L != oo:
                            lim_pos_ok = False
                            
                    # Check if the sequence diverges to infinity as the variable goes to -oo
                    lim_neg_ok = True
                    if getattr(base, 'inf', None) == -oo:
                        L = limit(Abs(expr), var, -oo)
                        if L != oo:
                            lim_neg_ok = False
                            
                    if lim_pos_ok and lim_neg_ok:
                        return True
        except Exception:
            pass
            
    return False

def conditions(witness) -> list[bool]:
    # H_1: S is a subset of the real numbers R
    try:
        h1 = bool(witness.is_subset(S.Reals))
    except Exception:
        h1 = False

    # H_2: S is an infinite set
    try:
        h2 = False
        if getattr(witness, 'is_finite', None) is False:
            h2 = True
        elif getattr(witness, 'is_infinite', None) is True:
            h2 = True
        elif isinstance(witness, ImageSet):
            base = witness.base_sets[0]
            if getattr(base, 'is_finite', None) is False:
                expr = witness.lamda.expr
                # If the expression is not a constant, the image of an infinite set is typically infinite
                if len(expr.free_symbols) > 0:
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: S does NOT have at least one accumulation point in R
    try:
        neg_q = has_no_accumulation_points(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a subset of the real numbers",
    "H_2: S is an infinite set",
    "¬Q: S has no accumulation points in R"
]

N_HYP = 2
NEG_Q_INDEX = 2