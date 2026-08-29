import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def _check_attr(witness, names, default):
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                return witness[name]
        return default
    else:
        for name in names:
            if hasattr(witness, name):
                val = getattr(witness, name)
                return val() if callable(val) else val
        return default

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    Since SymPy does not natively support infinite Galois theory or Krull topologies,
    this verifier inspects the properties of a mock witness object or dictionary.
    """
    # H_1: E/F is a Galois extension (possibly infinite)
    try:
        if isinstance(witness, str):
            s = witness.lower()
            h1 = "galois" in s
        else:
            h1 = bool(_check_attr(witness, ['is_galois', 'is_galois_extension', 'galois'], False))
    except Exception:
        h1 = False

    # ¬Q: The maps do NOT define mutually inverse bijections between closed subgroups of G and intermediate fields
    try:
        if isinstance(witness, str):
            s = witness.lower()
            neg_q = "fail" in s or "discrete" in s or "not" in s or "no bijection" in s
        else:
            bij = _check_attr(witness, ['bijection_holds', 'conclusion_holds', 'is_bijection', 'conclusion'], True)
            neg_q = not bool(bij)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a Galois extension (possibly infinite)",
    "¬Q: The maps do not define mutually inverse bijections between closed subgroups of G and intermediate fields"
]

N_HYP = 1
NEG_Q_INDEX = 1