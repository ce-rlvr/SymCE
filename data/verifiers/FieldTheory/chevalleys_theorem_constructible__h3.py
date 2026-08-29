import sympy
from sympy import S, Complement, FiniteSet, Union, Intersection, Interval, ImageSet

# Top-level setup for potential witness expressions
CC = S.Complexes
QQ = S.Rationals
RR = S.Reals
ZZ = S.Integers
NN = S.Naturals

def get_attr_or_key(obj, key):
    if isinstance(obj, dict):
        return obj[key]
    return getattr(obj, key)

def is_alg_closed(K):
    if K == S.Complexes:
        return True
    if getattr(K, 'is_algebraically_closed', False):
        return True
    if isinstance(K, str) and K in ["C", "CC", "Complexes", "algebraically closed field"]:
        return True
    return False

def is_variety_over_K(V, K):
    if V == K:
        return True
    if isinstance(V, str) and V in ["A1", "A^1", "A1_K", "P1", "P^1", "variety"]:
        return True
    if getattr(V, 'is_variety', False):
        return True
    return False

def is_constructible_in_A1(subset, K):
    if subset == K or subset == S.EmptySet:
        return True
    if isinstance(subset, FiniteSet) or isinstance(subset, set):
        return True
    if isinstance(subset, Complement):
        base, excluded = subset.args
        if (base == K or base == S.Complexes) and isinstance(excluded, FiniteSet):
            return True
    if isinstance(subset, Union) or isinstance(subset, Intersection):
        return all(is_constructible_in_A1(arg, K) for arg in subset.args)
    if isinstance(subset, str) and subset in ["A1", "A^1", "empty", "K", "C", "CC", "point", "finite"]:
        return True
    if getattr(subset, 'is_constructible', False):
        return True
    return False

def is_subset_of_K(subset, K):
    if subset == K or subset == S.EmptySet:
        return True
    if isinstance(subset, FiniteSet) or isinstance(subset, set):
        return True
    if isinstance(subset, Complement):
        base, excluded = subset.args
        if base == K or base == S.Complexes:
            return True
    if isinstance(subset, Union) or isinstance(subset, Intersection):
        return all(is_subset_of_K(arg, K) for arg in subset.args)
    if isinstance(subset, ImageSet):
        return True
    if hasattr(subset, "is_subset"):
        try:
            if subset.is_subset(S.Complexes):
                return True
        except Exception:
            pass
    if subset in (S.Reals, S.Integers, S.Naturals, S.Naturals0, S.Rationals):
        return True
    if isinstance(subset, Interval):
        return True
    if isinstance(subset, str):
        if subset in ["R", "Reals", "Z", "Integers", "N", "Naturals", "Q", "Rationals", "half-plane", "unit-disk"]:
            return True
    if getattr(subset, 'is_subset', False):
        return True
    return False

def conditions(witness):
    try:
        K = get_attr_or_key(witness, "K")
        h1 = is_alg_closed(K)
    except Exception:
        h1 = False

    try:
        X = get_attr_or_key(witness, "X")
        Y = get_attr_or_key(witness, "Y")
        h2 = is_variety_over_K(X, K) and is_variety_over_K(Y, K)
    except Exception:
        h2 = False

    try:
        C = get_attr_or_key(witness, "C")
        h3 = is_constructible_in_A1(C, K) and is_subset_of_K(C, K)
    except Exception:
        h3 = False

    try:
        try:
            f_image = get_attr_or_key(witness, "f_image")
        except Exception:
            f = get_attr_or_key(witness, "f")
            C_val = get_attr_or_key(witness, "C")
            f_image = sympy.imageset(f, C_val)
            
        is_sub = is_subset_of_K(f_image, K)
        is_const = is_constructible_in_A1(f_image, K)
        neg_q = bool(is_sub and not is_const)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: X and Y are algebraic varieties over K",
    "H_3: C is a constructible set in X",
    "¬Q: The image f(C) is not a constructible set in Y"
]

N_HYP = 3
NEG_Q_INDEX = 3