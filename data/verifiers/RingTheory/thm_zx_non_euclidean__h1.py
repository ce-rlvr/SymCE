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

from sympy.abc import x

Zx = sympy.ZZ[x]

def conditions(witness):
    try:
        h1_ok = bool(witness == Zx)
    except Exception:
        h1_ok = False

    try:
        if getattr(witness, 'is_Field', False):
            neg_q_ok = True
        elif witness == sympy.ZZ:
            neg_q_ok = True
        elif hasattr(witness, 'domain') and hasattr(witness, 'gens') and len(witness.gens) == 1 and getattr(witness.domain, 'is_Field', False):
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: R is the polynomial ring over Z", "¬Q: R is a Euclidean domain"]
N_HYP = 1
NEG_Q_INDEX = 1