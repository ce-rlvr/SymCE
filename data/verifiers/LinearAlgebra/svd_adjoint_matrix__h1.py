import sympy
from sympy import simplify, Matrix, eye, zeros
from sympy.abc import x, y, z

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_nonzero(s):
    try:
        if s == 0:
            return False
        if hasattr(s, 'is_zero'):
            if s.is_zero is True:
                return False
            if s.is_zero is False:
                return True
        if hasattr(s, 'free_symbols') and not s.free_symbols:
            val = complex(s.evalf())
            if abs(val) < 1e-9:
                return False
        return simplify(s) != 0
    except Exception:
        return True

def is_equiv(a, b):
    try:
        if a == b:
            return True
        diff = a - b
        if diff == 0:
            return True
        if hasattr(diff, 'is_zero') and diff.is_zero is True:
            return True
        if hasattr(diff, 'free_symbols') and not diff.free_symbols:
            val = complex(diff.evalf())
            if abs(val) < 1e-9:
                return True
        if simplify(diff) == 0:
            return True
    except Exception:
        pass
    return False

def multiset_eq(list1, list2):
    if len(list1) != len(list2):
        return False
    l2 = list(list2)
    for item in list1:
        found = False
        for i, val in enumerate(l2):
            if is_equiv(item, val):
                l2.pop(i)
                found = True
                break
        if not found:
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, sigma_list = witness
        else:
            A = witness
            sigma_list = None
            
        if not hasattr(A, 'singular_values'):
            A = Matrix(A)
    except Exception:
        return [False, False]

    # H_1: sigma_1, ..., sigma_k are the non-zero singular values of A, where k = rank(A)
    try:
        actual_sigmas = [s for s in A.singular_values() if is_nonzero(s)]
        if sigma_list is not None:
            h1 = multiset_eq(sigma_list, actual_sigmas) and (len(sigma_list) == A.rank())
        else:
            sigma_list = actual_sigmas
            h1 = (len(sigma_list) == A.rank())
    except Exception:
        h1 = False

    # ¬Q: The conjugate transpose A* does NOT have exactly the same non-zero singular values as A
    try:
        ah_sigmas = [s for s in A.H.singular_values() if is_nonzero(s)]
        q = multiset_eq(ah_sigmas, sigma_list)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sigma_1, ..., sigma_k are the non-zero singular values of A, where k = rank(A)",
    "¬Q: The conjugate transpose A* does NOT have exactly the same non-zero singular values as A"
]

N_HYP = 1
NEG_Q_INDEX = 1