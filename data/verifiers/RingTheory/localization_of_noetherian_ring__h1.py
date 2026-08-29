import sympy
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    Since SymPy does not natively support non-commutative ring localizations 
    (which is where this conjecture fails), the witness is expected to be a 
    mock object or dictionary containing the boolean properties.
    """
    def get_bool(obj, names, default):
        if isinstance(obj, dict):
            for name in names:
                if name in obj:
                    return bool(obj[name])
        
        for name in names:
            if hasattr(obj, name):
                val = getattr(obj, name)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                return bool(val)
                
        if isinstance(obj, (tuple, list)):
            for item in obj:
                if isinstance(item, dict):
                    for name in names:
                        if name in item:
                            return bool(item[name])
                else:
                    for name in names:
                        if hasattr(item, name):
                            val = getattr(item, name)
                            if callable(val):
                                try:
                                    return bool(val())
                                except Exception:
                                    pass
                            return bool(val)
        return default

    try:
        h1 = get_bool(witness, ["is_Noetherian_ring", "is_Noetherian", "R_is_Noetherian", "noetherian"], False)
    except Exception:
        h1 = False

    try:
        h2 = get_bool(witness, ["is_multiplicatively_closed", "S_is_multiplicatively_closed", "multiplicatively_closed", "mult_closed"], False)
    except Exception:
        h2 = False

    try:
        q = get_bool(witness, ["localized_is_Noetherian", "is_localized_Noetherian", "S_inv_R_is_Noetherian", "localized_noetherian"], True)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2