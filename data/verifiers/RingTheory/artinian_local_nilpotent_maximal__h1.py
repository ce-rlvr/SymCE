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
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard algebra objects
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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a local ring with a non-nilpotent maximal ideal.
    """
    # 1. Witness as a prime integer representing the local ring Z_{(p)}
    try:
        if isinstance(witness, (int, Integer)):
            if sympy.isprime(witness):
                # Z_{(p)} is local, and its maximal ideal pZ_{(p)} is not nilpotent
                return [True, True]
    except Exception:
        pass

    # 2. Witness as a tuple (ring_type, parameter)
    try:
        if isinstance(witness, tuple) and len(witness) >= 1:
            rtype = witness[0]
            if rtype == "Z_(p)":
                p = Integer(witness[1])
                if sympy.isprime(p):
                    return [True, True]
            elif rtype == "Z_n":
                n = Integer(witness[1])
                factors = sympy.factorint(n)
                if len(factors) == 1:
                    # Z_n for n=p^k is local, but its maximal ideal IS nilpotent
                    return [True, False]
                else:
                    return [False, False]
            elif rtype in ("k[[x]]", "k[x]_(x)", "power_series"):
                return [True, True]
    except Exception:
        pass

    # 3. Witness as a string description
    try:
        if isinstance(witness, str):
            w = witness.lower()
            if "z_(p)" in w or "k[[x]]" in w or "k[x]_(x)" in w:
                return [True, True]
    except Exception:
        pass

    # 4. Witness as a SymPy Field
    try:
        if hasattr(witness, 'is_Field') and witness.is_Field:
            # Fields are local rings, but their maximal ideal (0) is nilpotent
            return [True, False]
    except Exception:
        pass

    # 5. Witness as a dictionary
    try:
        if isinstance(witness, dict):
            is_local = bool(witness.get('is_local', witness.get('is_local_ring', False)))
            is_nilpotent = bool(witness.get('is_nilpotent', witness.get('maximal_ideal_is_nilpotent', True)))
            return [is_local, not is_nilpotent]
    except Exception:
        pass

    # 6. Witness as an object with attributes
    try:
        if hasattr(witness, 'is_local') or hasattr(witness, 'is_local_ring'):
            is_local = bool(getattr(witness, 'is_local', getattr(witness, 'is_local_ring', False)))
            is_nilpotent = bool(getattr(witness, 'is_nilpotent', getattr(witness, 'maximal_ideal_is_nilpotent', True)))
            return [is_local, not is_nilpotent]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: R is a local ring with unique maximal ideal m",
    "¬Q: The maximal ideal m is not nilpotent"
]

N_HYP = 1
NEG_Q_INDEX = 1