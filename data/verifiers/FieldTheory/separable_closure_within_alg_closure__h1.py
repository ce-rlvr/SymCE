import sympy
from sympy import *
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _get_bool_attr(witness, *names, default=False):
    """Helper to extract boolean properties from a mock witness object or dictionary."""
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                return bool(witness[name])
    else:
        for name in names:
            if hasattr(witness, name):
                val = getattr(witness, name)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since SymPy lacks native structures for arbitrary algebraic and separable closures,
    this verifier expects a mock object or dictionary representing the counterexample's properties.
    """
    # H_1: \overline{F} is an algebraic closure of F
    try:
        h1 = _get_bool_attr(witness, 'is_algebraic_closure', 'F_bar_is_algebraic_closure', 'h1', default=False)
    except Exception:
        h1 = False

    # H_2: F^{sep} is the set of all elements in \overline{F} that are separable over F
    try:
        h2 = _get_bool_attr(witness, 'is_separable_elements', 'F_sep_is_separable_elements', 'h2', default=False)
    except Exception:
        h2 = False

    # ¬Q: F^{sep} is NOT a subfield of \overline{F} OR is NOT separably closed
    try:
        if isinstance(witness, dict) and 'q' in witness:
            neg_q = not bool(witness['q'])
        elif hasattr(witness, 'q'):
            val = getattr(witness, 'q')
            if callable(val):
                neg_q = not bool(val())
            else:
                neg_q = not bool(val)
        else:
            is_subfield = _get_bool_attr(witness, 'is_subfield', 'F_sep_is_subfield', 'q1', default=True)
            is_sep_closed = _get_bool_attr(witness, 'is_separably_closed', 'F_sep_is_separably_closed', 'q2', default=True)
            neg_q = not (is_subfield and is_sep_closed)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: \\overline{F} is an algebraic closure of F",
    "H_2: F^{sep} is the set of all elements in \\overline{F} that are separable over F",
    "¬Q: F^{sep} is not a subfield of \\overline{F} or is not separably closed"
]

N_HYP = 2
NEG_Q_INDEX = 2