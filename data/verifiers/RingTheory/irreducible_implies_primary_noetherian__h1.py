import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import z3
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

def get_val(obj, name, *args):
    """Helper to safely extract and evaluate a property or method from an object or dict."""
    if isinstance(obj, dict) and name in obj:
        val = obj[name]
        if callable(val):
            try:
                return bool(val(*args))
            except Exception:
                return bool(val())
        return bool(val)
    if hasattr(obj, name):
        attr = getattr(obj, name)
        if callable(attr):
            try:
                return bool(attr(*args))
            except Exception:
                return bool(attr())
        return bool(attr)
    return None

def evaluate_condition(witness, *names):
    """Attempts to evaluate a mathematical property on the witness using common naming conventions."""
    for name in names:
        # 1. Check if the witness itself has the property/method
        val = get_val(witness, name)
        if val is not None:
            return val
            
        # 2. Check if the witness is a callable that answers property queries
        if callable(witness):
            try:
                res = witness(name)
                if res is not None:
                    return bool(res)
            except Exception:
                pass
                
        # 3. Check if the witness is a tuple (Ring, Ideal)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            # Try evaluating on the ring, passing the ideal as an argument if it's a method
            val = get_val(R, name, I)
            if val is not None:
                return val
            # Try evaluating directly on the ideal
            val = get_val(I, name)
            if val is not None:
                return val

    raise AttributeError(f"Could not evaluate any of the properties: {names}")

def conditions(witness) -> list[bool]:
    # H_1: R is a Noetherian ring
    try:
        h1 = evaluate_condition(witness, 'is_noetherian', 'is_noetherian_ring')
    except Exception:
        h1 = False

    # H_2: I is a proper ideal of R
    try:
        h2 = evaluate_condition(witness, 'is_proper_ideal', 'is_proper')
    except Exception:
        h2 = False

    # H_3: I is an irreducible ideal
    try:
        h3 = evaluate_condition(witness, 'is_irreducible_ideal', 'is_irreducible')
    except Exception:
        h3 = False

    # ¬Q: I is NOT a primary ideal
    try:
        q = evaluate_condition(witness, 'is_primary_ideal', 'is_primary')
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: I is a proper ideal of R",
    "H_3: I is an irreducible ideal",
    "¬Q: I is not a primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3