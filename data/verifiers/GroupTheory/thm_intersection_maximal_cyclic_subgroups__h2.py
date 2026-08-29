import sympy
from sympy.combinatorics import free_group

# Top-level setup: define a default free group and generators 
# so that witness expressions can easily reference them.
F, x, y = free_group("x, y")
FreeGroup = type(F)
FreeGroupElement = type(F.identity)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "In a free group F, if A and B are subgroups and A != B, then their intersection is trivial."
    (The dropped hypothesis was that A and B are *maximal* cyclic subgroups).
    
    The witness is expected to provide two elements `a` and `b` of a free group,
    representing the cyclic subgroups A = <a> and B = <b>.
    The witness can be a tuple (a, b) or (F, a, b).
    Lists of length 1 like ([a], [b]) are also accepted.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                _, A, B = witness
            elif len(witness) == 2:
                A, B = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        def get_gen(X):
            if isinstance(X, FreeGroupElement):
                return X
            if isinstance(X, (list, tuple, set)) and len(X) == 1:
                elem = list(X)[0]
                if isinstance(elem, FreeGroupElement):
                    return elem
            return None
            
        a = get_gen(A)
        b = get_gen(B)
        
        if a is None or b is None:
            return [False, False, False]
            
        F_wit = a.group
        if F_wit != b.group:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H_1: F is a free group
    try:
        h1 = isinstance(F_wit, FreeGroup)
    except Exception:
        h1 = False

    # H_2: A is not equal to B
    # A and B are the cyclic subgroups <a> and <b>.
    # In a free group, <a> == <b> iff a == b or a == b**-1.
    try:
        h2 = not (a == b or a == b**-1)
    except Exception:
        h2 = False

    # ¬Q: The intersection of A and B is not the trivial subgroup
    # For cyclic subgroups in a free group, <a> and <b> intersect non-trivially
    # iff a and b are non-trivial and they commute.
    try:
        neg_q = False
        if a != F_wit.identity and b != F_wit.identity:
            if a * b == b * a:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: A is not equal to B",
    "¬Q: The intersection of A and B is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2