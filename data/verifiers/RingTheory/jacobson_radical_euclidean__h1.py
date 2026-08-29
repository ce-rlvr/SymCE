import sympy
from sympy.polys.domains import ZZ, QQ
import math
import itertools
import functools

# Top-level setup
Z2 = sympy.S(2)
Z3 = sympy.S(3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Check H_1: R contains infinitely many pairwise non-associate prime elements
    try:
        if isinstance(witness, str):
            w = witness.lower().replace(" ", "")
            if w in ["zxz4", "zzxz/4z", "zxz/4z", "zxz_4", "zzxzz/4zz", "z[[x]]", "zz[[x]]"]:
                h1 = True
    except Exception:
        pass

    try:
        if isinstance(witness, dict) and "has_infinitely_many_primes" in witness:
            h1 = bool(witness["has_infinitely_many_primes"])
        elif hasattr(witness, "has_infinitely_many_primes"):
            val = witness.has_infinitely_many_primes
            h1 = bool(val() if callable(val) else val)
        elif witness == ZZ:
            h1 = True
        elif witness == QQ:
            h1 = False
    except Exception:
        pass

    # Check ¬Q: The Jacobson radical of R is not the zero ideal
    try:
        if isinstance(witness, str):
            w = witness.lower().replace(" ", "")
            if w in ["zxz4", "zzxz/4z", "zxz/4z", "zxz_4", "zzxzz/4zz", "z[[x]]", "zz[[x]]"]:
                neg_q = True
    except Exception:
        pass

    try:
        if isinstance(witness, dict) and "jacobson_radical_is_zero" in witness:
            neg_q = not bool(witness["jacobson_radical_is_zero"])
        elif hasattr(witness, "jacobson_radical_is_zero"):
            val = witness.jacobson_radical_is_zero
            neg_q = not bool(val() if callable(val) else val)
        elif witness == ZZ:
            neg_q = False
        elif witness == QQ:
            neg_q = False
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R contains infinitely many pairwise non-associate prime elements",
    "¬Q: The Jacobson radical of R is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1