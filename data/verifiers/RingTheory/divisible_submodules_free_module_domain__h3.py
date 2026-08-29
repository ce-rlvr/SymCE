import sympy

ZZ = sympy.ZZ
QQ = sympy.QQ

def check_divisible(R, M):
    try:
        if M == QQ and R == ZZ:
            return True
    except Exception:
        pass
    try:
        if hasattr(M, 'is_divisible_module_over'):
            return bool(M.is_divisible_module_over(R))
    except Exception:
        pass
    try:
        if hasattr(R, 'get_field') and M == R.get_field():
            return True
    except Exception:
        pass
    try:
        if getattr(M, 'is_Field', False) and hasattr(R, 'is_subset') and R.is_subset(M):
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        elif isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M')
        else:
            R = getattr(witness, 'R', None)
            M = getattr(witness, 'M', None)
            
        if R is None or M is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is an integral domain
    try:
        if R == ZZ:
            h1 = True
        elif hasattr(R, 'is_integral_domain'):
            h1 = bool(R.is_integral_domain)
        else:
            h1 = hasattr(R, 'get_field') and callable(R.get_field)
    except Exception:
        h1 = False

    # H2: R is not a field
    try:
        if R == ZZ:
            h2 = True
        elif hasattr(R, 'is_field'):
            h2 = not bool(R.is_field)
        elif hasattr(R, 'is_Field'):
            h2 = not bool(R.is_Field)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: M contains a non-zero divisible submodule
    try:
        neg_q = False
        if hasattr(witness, 'has_nonzero_divisible_submodule'):
            neg_q = bool(witness.has_nonzero_divisible_submodule())
        elif check_divisible(R, M):
            neg_q = True
        elif isinstance(M, (list, tuple, set)):
            for m in M:
                if check_divisible(R, m):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R is not a field",
    "¬Q: M contains a non-zero divisible submodule"
]

N_HYP = 2
NEG_Q_INDEX = 2