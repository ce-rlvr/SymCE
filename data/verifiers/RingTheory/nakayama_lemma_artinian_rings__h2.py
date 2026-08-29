import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
from sympy import Rational, Integer
import sympy.ntheory
import math
import itertools
import functools
import z3

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
    h1 = False
    h2 = False
    neg_q = False
    
    # 1. Check if witness is a dictionary
    try:
        if isinstance(witness, dict):
            if 'is_right_Artinian' in witness or 'M_J_equals_M' in witness:
                h1 = bool(witness.get('is_right_Artinian', False))
                h2 = bool(witness.get('M_J_equals_M', False))
                neg_q = not bool(witness.get('is_zero_module', True))
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Check if witness is a tuple (R, M) representing Z/nZ and a direct sum of Z/mZ
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            if isinstance(R, (int, sympy.Integer)):
                R_val = int(R)
                if isinstance(M, (int, sympy.Integer)):
                    M_list = [int(M)]
                elif isinstance(M, list) and all(isinstance(val, (int, sympy.Integer)) for val in M):
                    M_list = [int(val) for val in M]
                else:
                    M_list = None
                
                if M_list is not None:
                    if R_val != 0:
                        h1 = True
                        # For M to be a valid R-module, R must annihilate M
                        if all(m != 0 and R_val % m == 0 for m in M_list):
                            factors = sympy.ntheory.factorint(abs(R_val))
                            rad_R = math.prod(factors.keys()) if factors else 1
                            h2 = all(math.gcd(rad_R, m) == 1 for m in M_list)
                        else:
                            h2 = False
                        neg_q = not all(abs(m) == 1 for m in M_list)
                        return [h1, h2, neg_q]
                    else:
                        # R = 0 means Z, which is not Artinian
                        h1 = False
                        h2 = False
                        neg_q = not all(abs(m) == 1 for m in M_list if m != 0) or any(m == 0 for m in M_list)
                        return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Check if witness is an object with attributes
    try:
        h1 = bool(getattr(witness, 'is_right_Artinian', False) or getattr(witness, 'is_artinian', False))
    except Exception:
        pass

    try:
        h2 = bool(getattr(witness, 'M_J_equals_M', False) or getattr(witness, 'm_j_equals_m', False))
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_zero_module'):
            neg_q = not bool(witness.is_zero_module)
        elif hasattr(witness, 'is_zero'):
            neg_q = not bool(witness.is_zero)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "H_2: M J(R) = M, where J(R) is the Jacobson radical of R",
    "¬Q: The module M is not the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2