import sympy
from sympy.abc import x, y, z

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a tuple (R, I_gen) where R is a SymPy domain and I_gen generates the ideal,
    or simply I_gen (in which case R is assumed to be ZZ).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I_gen = witness
        else:
            R = ZZ
            I_gen = witness
    except Exception:
        return [False, False, False]

    # H_1: R is an integral domain
    try:
        h1 = False
        if R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            d = R
            while hasattr(d, 'domain'):
                d = d.domain
            if d in (ZZ, QQ) or (hasattr(d, 'is_Field') and d.is_Field):
                h1 = True
    except Exception:
        h1 = False

    # H_2: R is a Dedekind domain
    try:
        h2 = False
        if R in (ZZ, QQ):
            h2 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h2 = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            if len(R.symbols) == 1:
                k = R.domain
                if k == QQ or (hasattr(k, 'is_Field') and k.is_Field):
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: I is not an invertible fractional ideal
    # In a Dedekind domain, a fractional ideal is invertible if and only if it is non-zero.
    try:
        if isinstance(I_gen, (list, tuple, set)):
            is_zero = all(g == 0 for g in I_gen)
        elif hasattr(I_gen, 'is_zero') and I_gen.is_zero is not None:
            is_zero = I_gen.is_zero
        elif hasattr(I_gen, 'gens'):
            is_zero = all(g == 0 for g in I_gen.gens)
        else:
            is_zero = (I_gen == 0)
        
        neg_q = bool(is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R is a Dedekind domain",
    "¬Q: I is not an invertible fractional ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2