import sympy
from sympy import S, Interval, FiniteSet, Union, Intersection, ProductSet

Reals = S.Reals
oo = sympy.oo

def is_bounded(K):
    if K == S.EmptySet:
        return True
    if getattr(K, 'is_FiniteSet', False):
        return True
    if isinstance(K, ProductSet):
        return all(is_bounded(s) for s in K.sets)
    if isinstance(K, Union):
        return all(is_bounded(s) for s in K.args)
    if isinstance(K, Intersection):
        return any(is_bounded(s) for s in K.args)
    
    try:
        from sympy.geometry import GeometryEntity, Line, Ray, Parabola, Line3D, Ray3D, Plane
        if isinstance(K, GeometryEntity):
            if isinstance(K, (Line, Ray, Parabola, Line3D, Ray3D, Plane)):
                return False
            return True
    except Exception:
        pass

    if hasattr(K, 'inf') and hasattr(K, 'sup'):
        inf_val = K.inf
        sup_val = K.sup
        if inf_val is not None and sup_val is not None:
            try:
                return bool(inf_val.is_finite and sup_val.is_finite)
            except Exception:
                pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                K, epsilon = witness
            elif len(witness) == 3:
                K, n, epsilon = witness
            else:
                K, epsilon = None, None
        else:
            K, epsilon = None, None
    except Exception:
        K, epsilon = None, None

    # H_1: epsilon is a strictly positive real number
    h1_ok = False
    try:
        if epsilon is not None:
            eps_sym = sympy.sympify(epsilon)
            if eps_sym.is_real and eps_sym.is_positive:
                h1_ok = True
    except Exception:
        pass

    # neg_Q: K cannot be covered by finitely many open balls of radius epsilon
    # In R^n, this is equivalent to K being unbounded.
    neg_q_ok = False
    try:
        if K is not None and isinstance(K, sympy.Set):
            neg_q_ok = not is_bounded(K)
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: epsilon is a strictly positive real number",
    "¬Q: K cannot be covered by finitely many open balls of radius epsilon (K is unbounded)"
]

N_HYP = 1
NEG_Q_INDEX = 1