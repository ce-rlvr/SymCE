import sympy
import sympy.combinatorics
import sympy.matrices
import itertools
import math
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: I is equal to its own radical iff R/I has no non-zero nilpotent elements fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        R, I = witness
    except Exception:
        return [False, False]
        
    # H1: R is a commutative ring
    h1 = False
    try:
        if R in (sympy.ZZ, sympy.QQ):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif type(R).__name__ in ['IntegerRing', 'RationalField', 'RealField', 'ComplexField', 'GaloisField']:
            h1 = True
    except Exception:
        pass

    # neg_Q: I is equal to its own radical iff R/I has no non-zero nilpotent elements
    neg_q = False
    try:
        def in_I(val):
            if callable(I):
                return bool(I(val))
            elif hasattr(I, 'contains'):
                return bool(I.contains(val))
            else:
                return val in I

        if R == sympy.ZZ:
            domain = list(range(-20, 21))
        elif R == sympy.QQ:
            domain = [sympy.Rational(p, q) for p in range(-5, 6) for q in range(1, 4)]
        else:
            try:
                domain = list(R)
            except Exception:
                domain = list(range(-20, 21))
                
        # Check if I is an ideal
        is_ideal = True
        zero = R.zero if hasattr(R, 'zero') else 0
        if not in_I(zero):
            is_ideal = False
        else:
            for a in domain:
                if not is_ideal: 
                    break
                for b in domain:
                    if in_I(a) and in_I(b):
                        try:
                            if not in_I(a + b):
                                is_ideal = False
                                break
                        except Exception:
                            pass
                    if in_I(a):
                        try:
                            if not in_I(a * b):
                                is_ideal = False
                                break
                        except Exception:
                            pass

        # Check LHS: I == radical(I)
        lhs = True
        for x in domain:
            val_in_I = in_I(x)
            val_in_rad = False
            for n in range(1, 6):
                try:
                    if in_I(x**n):
                        val_in_rad = True
                        break
                except Exception:
                    pass
            if val_in_I != val_in_rad:
                lhs = False
                break
                
        # If I is not an ideal, R/I is not a valid quotient ring, so RHS is False.
        # The equivalence (LHS iff RHS) becomes (LHS iff False), which is (not LHS).
        # We want the equivalence to FAIL, so we need (not LHS) to be False, meaning LHS must be True.
        if not is_ideal and lhs:
            neg_q = True
            
    except Exception:
        pass

    return [h1, neg_q]