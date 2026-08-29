import math
import itertools
import functools
import sympy
from sympy import eye, zeros, Rational, Integer, Matrix
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a finitely generated module over R",
    "¬Q: T is not a direct summand of M"
]

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    # 1. Check if witness is a dictionary (mock object)
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_PID", False))
            h2 = bool(witness.get("is_finitely_generated", False))
            if "torsion_is_direct_summand" in witness:
                neg_q = not bool(witness["torsion_is_direct_summand"])
            elif "torsion_splits" in witness:
                neg_q = not bool(witness["torsion_splits"])
            else:
                neg_q = bool(witness.get("neg_q", False))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Check if witness is a Sympy Matrix (representing a presentation matrix over Z)
    try:
        if isinstance(witness, Matrix):
            h1 = True  # Z is a PID
            h2 = True  # Finite presentation matrix implies finitely generated
            neg_q = False  # Finitely generated modules over Z always split
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Check if witness is a tuple (ring, module)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, mod = witness
            if hasattr(ring, "is_PID"):
                h1 = bool(ring.is_PID)
            elif str(ring) in ["ZZ", "Z", "Integers"]:
                h1 = True
            
            if isinstance(mod, Matrix):
                h2 = True
                neg_q = False
            elif hasattr(mod, "is_finitely_generated"):
                h2 = bool(mod.is_finitely_generated)
                if hasattr(mod, "torsion_is_direct_summand"):
                    neg_q = not bool(mod.torsion_is_direct_summand)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 4. Check if witness is an object with attributes
    try:
        if hasattr(witness, "is_PID"):
            h1 = bool(witness.is_PID)
        elif hasattr(witness, "is_principal_ideal_domain"):
            h1 = bool(witness.is_principal_ideal_domain)
    except Exception:
        pass

    try:
        if hasattr(witness, "is_finitely_generated"):
            h2 = bool(witness.is_finitely_generated)
    except Exception:
        pass

    try:
        if hasattr(witness, "torsion_is_direct_summand"):
            neg_q = not bool(witness.torsion_is_direct_summand)
        elif hasattr(witness, "torsion_splits"):
            neg_q = not bool(witness.torsion_splits)
        elif hasattr(witness, "is_torsion_direct_summand"):
            neg_q = not bool(witness.is_torsion_direct_summand)
    except Exception:
        pass

    return [h1, h2, neg_q]