import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = witness.get('x')
            y = witness.get('y')
            z = witness.get('z')
            p = witness.get('p')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                x, y, z, p = witness
            elif len(witness) == 3:
                x, y, z = witness
                p = None
            else:
                return [False, False]
        else:
            return [False, False]

        if p is None:
            for test_p in range(1, 100):
                try:
                    if int(str(x))**test_p + int(str(y))**test_p == int(str(z))**test_p:
                        p = test_p
                        break
                except Exception:
                    pass
            if p is None:
                p = 2

        h1 = False
        try:
            x_i = int(str(x))
            y_i = int(str(y))
            z_i = int(str(z))
            p_i = int(str(p))
            if p_i > 0 and p_i < 10000:
                h1 = (x_i**p_i + y_i**p_i == z_i**p_i)
        except Exception:
            h1 = False

        neg_q = False
        try:
            x_i = int(str(x))
            y_i = int(str(y))
            z_i = int(str(z))
            neg_q = (x_i * y_i * z_i != 0)
        except Exception:
            neg_q = False

        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: x, y, z are integers satisfying the equation x^p + y^p = z^p",
    "¬Q: The product xyz is not equal to 0"
]

N_HYP = 1
NEG_Q_INDEX = 1