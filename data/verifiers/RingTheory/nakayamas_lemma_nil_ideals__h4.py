import sympy
from sympy import ZZ, QQ

# Top-level setup
Z = ZZ
Q = QQ

def conditions(witness):
    try:
        R, I_gens, M_gens = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: R is a commutative ring
    try:
        if R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: I is a nil ideal of R
    try:
        h2 = True
        if not isinstance(I_gens, (list, tuple)):
            h2 = False
        else:
            for gen in I_gens:
                is_nil = False
                p = gen
                for _ in range(100):
                    if p == 0 or (hasattr(R, 'zero') and p == R.zero):
                        is_nil = True
                        break
                    p = p * gen
                if not is_nil:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: M is a finitely generated R-module
    try:
        h3 = isinstance(M_gens, (list, tuple))
    except Exception:
        h3 = False

    # neg_Q: M is not the zero module
    try:
        is_zero = True
        if not isinstance(M_gens, (list, tuple)):
            is_zero = False
        else:
            for m in M_gens:
                if isinstance(m, (list, tuple)):
                    if any(c != 0 and (not hasattr(R, 'zero') or c != R.zero) for c in m):
                        is_zero = False
                        break
                else:
                    if m != 0 and (not hasattr(R, 'zero') or m != R.zero):
                        is_zero = False
                        break
        neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is a nil ideal of R",
    "H_3: M is a finitely generated R-module",
    "¬Q: M is not the zero module"
]

N_HYP = 3
NEG_Q_INDEX = 3