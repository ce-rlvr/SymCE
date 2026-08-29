import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup
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
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('K_is_field', True))
            h2 = bool(witness.get('V_is_vector_space', True))
            h3 = bool(witness.get('omega_in_exterior_algebra', True))
            
            omega_is_unit = bool(witness.get('omega_is_unit', False))
            if 'omega_0_nonzero' in witness:
                omega_0_nonzero = bool(witness['omega_0_nonzero'])
            elif 'omega_0' in witness:
                omega_0_nonzero = bool(witness['omega_0'] != 0)
            else:
                omega_0_nonzero = False
                
            neg_q = (omega_is_unit != omega_0_nonzero)
            return [h1, h2, h3, neg_q]

        if hasattr(witness, 'omega_is_unit') or hasattr(witness, 'is_unit') or hasattr(witness, 'omega_0'):
            h1 = bool(getattr(witness, 'K_is_field', True))
            h2 = bool(getattr(witness, 'V_is_vector_space', True))
            h3 = bool(getattr(witness, 'omega_in_exterior_algebra', True))
            
            if hasattr(witness, 'omega_is_unit'):
                omega_is_unit = bool(witness.omega_is_unit() if callable(witness.omega_is_unit) else witness.omega_is_unit)
            elif hasattr(witness, 'is_unit'):
                omega_is_unit = bool(witness.is_unit() if callable(witness.is_unit) else witness.is_unit)
            else:
                omega_is_unit = False

            if hasattr(witness, 'omega_0_nonzero'):
                omega_0_nonzero = bool(witness.omega_0_nonzero() if callable(witness.omega_0_nonzero) else witness.omega_0_nonzero)
            elif hasattr(witness, 'omega_0'):
                omega_0 = witness.omega_0() if callable(witness.omega_0) else witness.omega_0
                omega_0_nonzero = bool(omega_0 != 0)
            else:
                omega_0_nonzero = False

            neg_q = (omega_is_unit != omega_0_nonzero)
            return [h1, h2, h3, neg_q]

    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: V is a vector space over K",
    "H_3: omega is in the exterior algebra of V with degree-zero component omega_0 and positive-degree component omega_+",
    "¬Q: omega is a unit in the exterior algebra if and only if omega_0 is non-zero is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3