import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
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
    Given a witness object, checks whether it is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    # H_1: R is a commutative ring
    h1_ok = False
    try:
        if hasattr(witness, 'is_commutative_ring'):
            h1_ok = bool(witness.is_commutative_ring())
        elif isinstance(witness, dict) and 'is_commutative_ring' in witness:
            h1_ok = bool(witness['is_commutative_ring'])
        elif hasattr(witness, 'R') and hasattr(witness.R, 'is_commutative'):
            h1_ok = bool(witness.R.is_commutative)
    except Exception:
        h1_ok = False

    # H_2: M is a simple R-module
    h2_ok = False
    try:
        if hasattr(witness, 'is_simple_module'):
            h2_ok = bool(witness.is_simple_module())
        elif isinstance(witness, dict) and 'is_simple_module' in witness:
            h2_ok = bool(witness['is_simple_module'])
        elif hasattr(witness, 'M') and hasattr(witness.M, 'is_simple'):
            h2_ok = bool(witness.M.is_simple)
    except Exception:
        h2_ok = False

    # neg_Q: The localized module S^{-1}M is NEITHER the zero module NOR a simple S^{-1}R-module.
    # This conclusion fails (i.e., neg_Q is True) typically when S is not a multiplicatively closed subset,
    # making S^{-1}R not a valid ring and S^{-1}M not a valid module.
    neg_q_ok = False
    try:
        if hasattr(witness, 'conclusion_holds'):
            neg_q_ok = not bool(witness.conclusion_holds())
        elif hasattr(witness, 'is_localized_module_zero') and hasattr(witness, 'is_localized_module_simple'):
            neg_q_ok = not (bool(witness.is_localized_module_zero()) or bool(witness.is_localized_module_simple()))
        elif isinstance(witness, dict) and 'conclusion_holds' in witness:
            neg_q_ok = not bool(witness['conclusion_holds'])
        elif hasattr(witness, 'S_is_multiplicatively_closed'):
            # If S is not multiplicatively closed, the localization is ill-defined and the conclusion fails.
            neg_q_ok = not bool(witness.S_is_multiplicatively_closed())
        elif hasattr(witness, 'S') and hasattr(witness, 'R') and hasattr(witness.R, 'mul'):
            # Attempt to manually check if S is multiplicatively closed
            S = witness.S
            R = witness.R
            is_closed = True
            for x in S:
                for y in S:
                    if R.mul(x, y) not in S:
                        is_closed = False
                        break
                if not is_closed:
                    break
            neg_q_ok = not is_closed
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is a simple R-module",
    "¬Q: The localized module S^{-1}M is neither the zero module nor a simple S^{-1}R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2