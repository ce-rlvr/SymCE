import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def extract_witness(witness):
    """
    Extracts the group F and the integer n from the witness.
    The witness can be a dictionary {'F': group, 'n': integer} or a tuple (F, n).
    """
    if isinstance(witness, dict):
        n = witness.get('n')
        if n is not None:
            try:
                n = int(n)
            except Exception:
                pass
        return witness.get('F'), n
    elif isinstance(witness, tuple) and len(witness) == 2:
        def is_int(x):
            return isinstance(x, int) or (hasattr(x, 'is_integer') and x.is_integer)
        
        if is_int(witness[0]) and not is_int(witness[1]):
            return witness[1], int(witness[0])
        elif is_int(witness[1]) and not is_int(witness[0]):
            return witness[0], int(witness[1])
        else:
            try:
                return witness[0], int(witness[1])
            except Exception:
                return witness[0], witness[1]
    return None, None

def conditions(witness) -> list[bool]:
    try:
        F, n = extract_witness(witness)
    except Exception:
        F, n = None, None

    # H_1: n is a positive integer
    try:
        h1_ok = isinstance(n, int) and n > 0
    except Exception:
        h1_ok = False

    # neg_Q: F does NOT contain a subgroup isomorphic to the free group of rank n
    try:
        neg_q_ok = False
        if h1_ok and F is not None:
            if isinstance(F, PermutationGroup):
                # Finite groups cannot contain a free group of rank n >= 1
                neg_q_ok = True
            elif hasattr(F, 'order'):
                order = F.order() if callable(F.order) else F.order
                if order < float('inf'):
                    neg_q_ok = True
            elif type(F).__name__ == 'FreeGroup':
                rank = len(F.generators)
                if rank == 0:
                    neg_q_ok = True
                elif rank == 1:
                    # Free group of rank 1 (Z) only contains subgroups of rank 1 or 0
                    neg_q_ok = (n != 1)
                else:
                    # Free groups of rank >= 2 contain free subgroups of any finite rank >= 1
                    neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: F does not contain a subgroup isomorphic to the free group of rank n"
]

N_HYP = 1
NEG_Q_INDEX = 1