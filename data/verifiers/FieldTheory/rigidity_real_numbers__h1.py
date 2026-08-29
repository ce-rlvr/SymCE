import sympy
import sympy.abc
import math
import itertools
import functools

x = sympy.abc.x

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        test_vals = [0, 1, -1, 2, sympy.Rational(1, 2), sympy.pi, sympy.E]
        for val in test_vals:
            try:
                if hasattr(witness, "subs"):
                    res = witness.subs(x, val)
                else:
                    res = witness(val)
                if sympy.simplify(res - val) != 0:
                    neg_q = True
                    break
            except Exception:
                pass
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sigma is not the identity map"
]

N_HYP = 0
NEG_Q_INDEX = 0