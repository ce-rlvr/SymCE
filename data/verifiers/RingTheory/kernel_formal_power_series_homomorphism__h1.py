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

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('h1', False))
            h2 = bool(witness.get('h2', False))
            neg_q = bool(witness.get('neg_q', False))
        elif hasattr(witness, 'h1') and hasattr(witness, 'h2') and hasattr(witness, 'neg_q'):
            h1 = bool(witness.h1)
            h2 = bool(witness.h2)
            neg_q = bool(witness.neg_q)
        elif isinstance(witness, tuple) and len(witness) == 3:
            if all(isinstance(item, bool) for item in witness):
                h1, h2, neg_q = witness
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism",
    "H_2: f_power_series is the induced homomorphism on the rings of formal power series",
    "¬Q: The kernel of f_power_series is not the ideal ker(f)_power_series"
]

N_HYP = 2
NEG_Q_INDEX = 2