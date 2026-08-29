import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
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

def conditions(witness):
    H1 = False
    neg_Q = False

    # 1. Custom object with methods/properties
    try:
        if hasattr(witness, 'is_P_primary'):
            H1 = witness.is_P_primary() if callable(witness.is_P_primary) else witness.is_P_primary
        elif hasattr(witness, 'H1'):
            H1 = witness.H1() if callable(witness.H1) else witness.H1
            
        if hasattr(witness, 'nilradical_equals_P_mod_Q'):
            neg_Q = not (witness.nilradical_equals_P_mod_Q() if callable(witness.nilradical_equals_P_mod_Q) else witness.nilradical_equals_P_mod_Q)
        elif hasattr(witness, 'nilradical_equals'):
            neg_Q = not (witness.nilradical_equals() if callable(witness.nilradical_equals) else witness.nilradical_equals)
        elif hasattr(witness, 'neg_Q'):
            neg_Q = witness.neg_Q() if callable(witness.neg_Q) else witness.neg_Q
            
        if H1 and neg_Q:
            return [True, True]
    except Exception:
        pass

    # 2. Dictionary representation
    try:
        if isinstance(witness, dict):
            if 'is_P_primary' in witness and 'nilradical_equals' in witness:
                H1 = bool(witness['is_P_primary'])
                neg_Q = not bool(witness['nilradical_equals'])
                if H1 and neg_Q:
                    return [True, True]
    except Exception:
        pass

    # 3. Tuple of (R, Q, P) representing a non-commutative ring (e.g., matrix ring)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, Q, P = witness
            
            def is_zero_ideal(I):
                if isinstance(I, list):
                    if len(I) != 1: return False
                    m = I[0]
                else:
                    m = I
                
                if m == 0: return True
                if hasattr(m, 'is_zero_matrix') and m.is_zero_matrix: return True
                if hasattr(m, 'is_zero') and m.is_zero: return True
                try:
                    return all(x == 0 for x in m)
                except Exception:
                    return False

            if is_zero_ideal(Q) and is_zero_ideal(P):
                # Check if R is explicitly marked as non-commutative
                if hasattr(R, 'is_commutative') and not R.is_commutative:
                    return [True, True]
                
                # Check if R has non-zero nilpotent elements (characteristic of matrix rings)
                has_nonzero_nilpotent = False
                try:
                    for m in R:
                        if is_zero_ideal(m): continue
                        
                        try:
                            m_pow = m
                            is_nilp = False
                            for _ in range(5):
                                m_pow = m_pow * m
                                if is_zero_ideal(m_pow):
                                    is_nilp = True
                                    break
                            if is_nilp:
                                has_nonzero_nilpotent = True
                                break
                        except Exception:
                            pass
                except TypeError:
                    pass
                
                if has_nonzero_nilpotent:
                    H1 = True
                    neg_Q = True
                    return [H1, neg_Q]
    except Exception:
        pass

    return [bool(H1), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: Q is a P-primary ideal in R",
    "¬Q: The nilradical of the quotient ring R/Q is not equal to P/Q"
]

N_HYP = 1
NEG_Q_INDEX = 1