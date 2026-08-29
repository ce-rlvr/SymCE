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

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: There is no bijection between the set of ideals of R containing I and the set of ideals of R/I"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    # 1. Duck-typing for custom objects
    try:
        if hasattr(witness, 'is_ideal'):
            h1 = witness.is_ideal()
        elif hasattr(witness, 'I_is_ideal'):
            h1 = witness.I_is_ideal
        elif isinstance(witness, dict) and 'I_is_ideal' in witness:
            h1 = witness['I_is_ideal']
    except Exception:
        pass

    try:
        if hasattr(witness, 'has_bijection'):
            neg_q = not witness.has_bijection()
        elif hasattr(witness, 'bijection'):
            neg_q = not witness.bijection
        elif isinstance(witness, dict) and 'bijection' in witness:
            neg_q = not witness['bijection']
    except Exception:
        pass

    if h1 or neg_q:
        return [bool(h1), bool(neg_q)]

    # 2. Finite ring as tuple (R, I)
    try:
        R, I = witness
        
        def contains(lst, elem):
            for e in lst:
                if e == elem:
                    return True
            return False

        # Check if I is a non-empty subset of R
        if I and all(contains(R, i) for i in I):
            # Check if I is a subgroup under addition
            is_subgroup = True
            for i1 in I:
                for i2 in I:
                    if not contains(I, i1 + i2):
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
            if is_subgroup:
                is_left = True
                for r in R:
                    for i in I:
                        if not contains(I, r * i):
                            is_left = False
                            break
                    if not is_left:
                        break

                is_right = True
                for r in R:
                    for i in I:
                        if not contains(I, i * r):
                            is_right = False
                            break
                    if not is_right:
                        break

                # H1: I is an ideal (at least one-sided)
                h1 = is_left or is_right
                
                # neg_Q: The bijection fails if it's not two-sided
                # because R/I is not a ring, so "ideals of R/I" is undefined or empty,
                # while ideals of R containing I might be non-empty.
                neg_q = not (is_left and is_right)
                
                return [bool(h1), bool(neg_q)]
    except Exception:
        pass

    # 3. SymPy rings
    try:
        R, I = witness
        if hasattr(I, 'is_ideal') and callable(I.is_ideal):
            h1 = I.is_ideal(R)
        elif type(I).__name__ == 'Ideal':
            h1 = True
            
        if h1:
            # For commutative rings in SymPy, ideals are always two-sided,
            # so the correspondence theorem holds, meaning neg_q is False.
            neg_q = False
            return [bool(h1), bool(neg_q)]
    except Exception:
        pass

    # 4. Callable witness
    try:
        if callable(witness):
            res = witness()
            if isinstance(res, (list, tuple)) and len(res) >= 2:
                return [bool(res[0]), bool(res[1])]
    except Exception:
        pass

    return [False, False]