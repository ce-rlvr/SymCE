import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
    # H_1: Let R be the ring of integers Z
    # We check if the witness is a function/dict representing d, or a tuple (R, d)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj, d_func = witness
            h1 = (R_obj == sympy.S.Integers or str(R_obj) in ["Z", "Integers", "ZZ"])
            witness_d = d_func
        else:
            h1 = callable(witness) or isinstance(witness, dict)
            witness_d = witness
    except Exception:
        h1 = False
        witness_d = witness

    # neg_Q: R is NOT a Euclidean domain with Euclidean function d
    # We verify if witness_d fails to be a valid Euclidean function on Z
    neg_q = False
    try:
        def get_val(x):
            if callable(witness_d):
                return witness_d(x)
            elif isinstance(witness_d, dict):
                return witness_d[x]
            else:
                raise ValueError

        is_euclidean = True
        
        # 1. Check domain and codomain: d must map Z \ {0} to non-negative integers
        for x in range(-30, 31):
            if x != 0:
                try:
                    val = get_val(x)
                    if isinstance(val, bool):
                        is_euclidean = False
                        break
                    val_int = int(val)
                    if val_int != val or val_int < 0:
                        is_euclidean = False
                        break
                except Exception:
                    is_euclidean = False
                    break
                    
        if is_euclidean:
            # 2. Check the division algorithm property
            for a in range(-30, 31):
                for b in range(-30, 31):
                    if b == 0:
                        continue
                    
                    try:
                        db = get_val(b)
                        db_float = float(db)
                    except Exception:
                        is_euclidean = False
                        break
                        
                    found = False
                    # Check a reasonable range for the quotient q
                    for q in range(-100, 101):
                        r = a - b * q
                        if r == 0:
                            found = True
                            break
                        try:
                            dr = get_val(r)
                            if isinstance(dr, bool):
                                continue
                            dr_int = int(dr)
                            # Valid remainder must have d(r) < d(b)
                            if dr_int == dr and dr_int >= 0 and dr_int < db_float:
                                found = True
                                break
                        except Exception:
                            pass
                    
                    if not found:
                        is_euclidean = False
                        break
                if not is_euclidean:
                    break
                    
        neg_q = not is_euclidean
    except Exception:
        # If evaluation fails fundamentally, it is not a valid Euclidean function
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is the ring of integers Z",
    "¬Q: R is not a Euclidean domain with Euclidean function d"
]

N_HYP = 1
NEG_Q_INDEX = 1