import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
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

CONDITION_LABELS = [
    "H_1: R is a reduced ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}R is not a reduced ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def check_R_S(R, S):
    h1 = False
    try:
        if hasattr(R, 'is_reduced'):
            h1 = R.is_reduced() if callable(R.is_reduced) else R.is_reduced
        elif hasattr(R, 'is_domain'):
            h1 = R.is_domain() if callable(R.is_domain) else R.is_domain
        else:
            h1_temp = True
            zero = R.zero if hasattr(R, 'zero') else 0
            elements = R.elements if hasattr(R, 'elements') else R
            for x in elements:
                if x != zero:
                    try:
                        if x * x == zero:
                            h1_temp = False
                            break
                    except Exception:
                        pass
            h1 = h1_temp
    except Exception:
        pass

    h2 = False
    try:
        if hasattr(S, 'is_multiplicatively_closed'):
            h2 = S.is_multiplicatively_closed() if callable(S.is_multiplicatively_closed) else S.is_multiplicatively_closed
        else:
            h2_temp = True
            for x in S:
                for y in S:
                    try:
                        if (x * y) not in S:
                            h2_temp = False
                            break
                    except Exception:
                        h2_temp = False
                        break
                if not h2_temp:
                    break
            h2 = h2_temp
    except Exception:
        pass

    neg_q = False
    try:
        zero = R.zero if hasattr(R, 'zero') else 0
        if zero in S:
            neg_q = True
        else:
            is_comm = True
            if hasattr(R, 'is_commutative'):
                is_comm = R.is_commutative() if callable(R.is_commutative) else R.is_commutative
            else:
                elements = R.elements if hasattr(R, 'elements') else R
                try:
                    for x in elements:
                        for y in elements:
                            try:
                                if x * y != y * x:
                                    is_comm = False
                                    break
                            except Exception:
                                pass
                        if not is_comm:
                            break
                except Exception:
                    pass
            if not is_comm:
                neg_q = True
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

def conditions(witness):
    if callable(witness):
        try:
            witness = witness()
        except Exception:
            pass

    # 1. Dictionary
    if isinstance(witness, dict):
        try:
            if 'is_reduced' in witness or 'localization_is_reduced' in witness:
                h1 = bool(witness.get('is_reduced', False))
                h2 = bool(witness.get('is_multiplicatively_closed', False))
                neg_q = not bool(witness.get('localization_is_reduced', True))
                return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Object with direct properties
    try:
        if hasattr(witness, 'localization_is_reduced') or hasattr(witness, 'is_localization_reduced'):
            h1 = False
            if hasattr(witness, 'is_reduced'):
                h1 = witness.is_reduced() if callable(witness.is_reduced) else witness.is_reduced
            elif hasattr(witness, 'R') and hasattr(witness.R, 'is_reduced'):
                h1 = witness.R.is_reduced() if callable(witness.R.is_reduced) else witness.R.is_reduced
                
            h2 = False
            if hasattr(witness, 'is_multiplicatively_closed'):
                h2 = witness.is_multiplicatively_closed() if callable(witness.is_multiplicatively_closed) else witness.is_multiplicatively_closed
            elif hasattr(witness, 'S_is_multiplicatively_closed'):
                h2 = witness.S_is_multiplicatively_closed() if callable(witness.S_is_multiplicatively_closed) else witness.S_is_multiplicatively_closed
            elif hasattr(witness, 'S') and hasattr(witness.S, 'is_multiplicatively_closed'):
                h2 = witness.S.is_multiplicatively_closed() if callable(witness.S.is_multiplicatively_closed) else witness.S.is_multiplicatively_closed
                
            neg_q = False
            if hasattr(witness, 'localization_is_reduced'):
                loc_red = witness.localization_is_reduced() if callable(witness.localization_is_reduced) else witness.localization_is_reduced
                neg_q = not loc_red
            elif hasattr(witness, 'is_localization_reduced'):
                loc_red = witness.is_localization_reduced() if callable(witness.is_localization_reduced) else witness.is_localization_reduced
                neg_q = not loc_red
                
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 3. Tuple (R, S)
    if isinstance(witness, tuple) and len(witness) == 2:
        return check_R_S(witness[0], witness[1])

    # 4. Object with R and S attributes
    if hasattr(witness, 'R') and hasattr(witness, 'S'):
        return check_R_S(witness.R, witness.S)

    return [False, False, False]