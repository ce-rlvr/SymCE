import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
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

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = True  # Z(R) being the center of R is definitional
    neg_q = False

    try:
        if isinstance(witness, type):
            witness = witness()
    except Exception:
        pass

    # Check if witness is a string describing the standard counterexample
    try:
        if isinstance(witness, str):
            s = witness.lower()
            if "infinite" in s and ("matrix" in s or "matrices" in s):
                h1 = True
                neg_q = True
            elif "weyl" in s:
                h1 = True
                neg_q = False
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Check if witness is a tuple (R, Z)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, Z = witness
            
            if hasattr(R, "is_simple"):
                h1 = bool(R.is_simple() if callable(R.is_simple) else R.is_simple)
            elif isinstance(R, dict):
                h1 = bool(R.get("is_simple", R.get("is_simple_ring", False)))
                
            if hasattr(Z, "is_field"):
                neg_q = not bool(Z.is_field() if callable(Z.is_field) else Z.is_field)
            elif isinstance(Z, dict):
                neg_q = not bool(Z.get("is_field", True))
            else:
                neg_q = (Z == 0 or str(Z) == "0")
                
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Check if witness is a dictionary
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_simple", witness.get("is_simple_ring", False)))
            if "center_is_field" in witness:
                neg_q = not bool(witness["center_is_field"])
            elif "center" in witness:
                center = witness["center"]
                if isinstance(center, dict) and "is_field" in center:
                    neg_q = not bool(center["is_field"])
                else:
                    neg_q = (center == 0 or str(center) == "0")
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Check if witness is a custom object with attributes/methods
    try:
        if hasattr(witness, "is_simple"):
            h1 = bool(witness.is_simple() if callable(witness.is_simple) else witness.is_simple)
        elif hasattr(witness, "is_simple_ring"):
            h1 = bool(witness.is_simple_ring() if callable(witness.is_simple_ring) else witness.is_simple_ring)
    except Exception:
        pass

    try:
        if hasattr(witness, "center_is_field"):
            cif = witness.center_is_field() if callable(witness.center_is_field) else witness.center_is_field
            neg_q = not bool(cif)
        elif hasattr(witness, "center"):
            center = witness.center() if callable(witness.center) else witness.center
            if hasattr(center, "is_field"):
                cif = center.is_field() if callable(center.is_field) else center.is_field
                neg_q = not bool(cif)
            elif center == 0 or str(center) == "0":
                neg_q = True
            else:
                neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a simple ring",
    "H_2: Z(R) is the center of R",
    "¬Q: Z(R) is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2