import sympy
from sympy import Symbol
from sympy.polys.domains import CC, QQ, ZZ, RR

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (K, L) or just L (in which case K is assumed to be CC).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K, L = witness
        else:
            K = CC
            L = witness
    except Exception:
        K, L = None, None

    # H_1: K is an algebraically closed field
    try:
        h1 = False
        if K is not None:
            is_k_field = getattr(K, 'is_Field', False) or getattr(K, 'is_field', False)
            if is_k_field:
                # In SymPy, CC is the standard algebraically closed field domain
                if str(K) == 'CC' or getattr(K, 'name', '') == 'CC':
                    h1 = True
    except Exception:
        h1 = False

    # H_2: L is an extension field of K
    try:
        h2 = False
        if K is not None and L is not None:
            is_l_field = getattr(L, 'is_Field', False) or getattr(L, 'is_field', False)
            if is_l_field:
                try:
                    # If L is an extension of K, unifying L and K should yield L
                    if L.unify(K) == L:
                        h2 = True
                except Exception:
                    pass
    except Exception:
        h2 = False

    # neg_Q: L is not equal to K
    try:
        neg_q = False
        if K is not None and L is not None:
            neg_q = (L != K)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: L is an extension field of K",
    "¬Q: L is not equal to K"
]

N_HYP = 2
NEG_Q_INDEX = 2