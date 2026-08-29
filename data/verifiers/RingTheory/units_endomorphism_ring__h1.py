import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_int(x):
    if isinstance(x, int):
        return True
    if hasattr(x, 'is_integer'):
        return x.is_integer is True
    return False

def check_is_unit(f):
    if isinstance(f, dict) and 'is_unit' in f:
        return bool(f['is_unit'])
    if hasattr(f, 'is_unit'):
        val = f.is_unit() if callable(f.is_unit) else f.is_unit
        if val is not None:
            return bool(val)
    if hasattr(f, 'is_square') and f.is_square:
        try:
            inv = f.inv()
            if all(is_int(x) for x in f) and not all(is_int(x) for x in inv):
                return False
            return True
        except Exception:
            return False
    return False

def check_is_automorphism(f):
    if isinstance(f, dict) and 'is_automorphism' in f:
        return bool(f['is_automorphism'])
    if hasattr(f, 'is_automorphism'):
        val = f.is_automorphism() if callable(f.is_automorphism) else f.is_automorphism
        if val is not None:
            return bool(val)
    if hasattr(f, 'is_square') and f.is_square:
        try:
            inv = f.inv()
            if all(is_int(x) for x in f) and not all(is_int(x) for x in inv):
                return False
            return True
        except Exception:
            return False
    return False

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture:
    'The endomorphism f is a unit in End_R(M) if and only if f is an R-module automorphism of M.'
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        M, f = witness
    else:
        M, f = None, witness

    # H_1: Let M be a left R-module.
    h1 = True
    if isinstance(witness, dict) and 'is_module' in witness:
        h1 = bool(witness['is_module'])

    # H_2: Let End_R(M) be the ring of R-module endomorphisms of M.
    h2 = True

    # H_3: Let f be an element of End_R(M).
    h3 = False
    try:
        if isinstance(f, dict) and 'is_endomorphism' in f:
            h3 = bool(f['is_endomorphism'])
        elif hasattr(f, 'is_square'):
            h3 = bool(f.is_square)
        elif hasattr(f, 'is_endomorphism'):
            val = f.is_endomorphism() if callable(f.is_endomorphism) else f.is_endomorphism
            h3 = bool(val)
        elif callable(f):
            h3 = True
        else:
            if isinstance(f, dict) or hasattr(f, 'is_unit'):
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails (f is a unit XOR f is an automorphism)
    try:
        u = check_is_unit(f)
        a = check_is_automorphism(f)
        neg_q = (u != a)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M is a left R-module",
    "H_2: End_R(M) is the ring of R-module endomorphisms of M",
    "H_3: f is an element of End_R(M)",
    "¬Q: f is a unit in End_R(M) XOR f is an R-module automorphism of M"
]

N_HYP = 3
NEG_Q_INDEX = 3