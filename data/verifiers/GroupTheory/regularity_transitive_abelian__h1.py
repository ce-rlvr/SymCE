import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings for witness expressions
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
    # H_1: G acts faithfully on a set \Omega
    # In SymPy, a PermutationGroup acts faithfully on its domain {0, 1, ..., degree-1}
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The action of G on \Omega is transitive
    try:
        if callable(witness.is_transitive):
            h2_ok = bool(witness.is_transitive())
        else:
            h2_ok = bool(witness.is_transitive)
    except Exception:
        h2_ok = False

    # ¬Q: The action of G on \Omega is not regular
    # Regular means the action is transitive and free (stabilizer of any point is trivial)
    try:
        if callable(witness.is_transitive):
            transitive = bool(witness.is_transitive())
        else:
            transitive = bool(witness.is_transitive)
            
        if callable(witness.degree):
            degree = int(witness.degree())
        else:
            degree = int(witness.degree)
            
        is_free = True
        if hasattr(witness, 'stabilizer'):
            for i in range(degree):
                stab = witness.stabilizer(i)
                if callable(stab.order):
                    stab_order = int(stab.order())
                else:
                    stab_order = int(stab.order)
                if stab_order > 1:
                    is_free = False
                    break
        else:
            # Fallback if stabilizer method is not available
            if callable(witness.order):
                order = int(witness.order())
            else:
                order = int(witness.order)
            is_free = (order == degree)
            
        is_regular = transitive and is_free
        neg_q_ok = not is_regular
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G acts faithfully on a set \\Omega",
    "H_2: The action of G on \\Omega is transitive",
    "¬Q: The action of G on \\Omega is not regular"
]

N_HYP = 2
NEG_Q_INDEX = 2