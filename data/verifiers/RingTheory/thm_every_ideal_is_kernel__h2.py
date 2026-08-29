import sympy
from sympy import S
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        R, I = witness
    except Exception:
        return [False, False]
        
    # H1: R is a ring
    try:
        h1 = False
        if isinstance(R, (int, sympy.Integer)) and int(R) >= 2:
            h1 = True
        elif hasattr(R, 'is_Ring') and R.is_Ring:
            h1 = True
        elif R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            h1 = True
        elif hasattr(R, 'is_ring') and R.is_ring:
            h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: I is not the kernel of any surjective ring homomorphism from R
    # This is mathematically equivalent to checking that I is NOT an ideal of R.
    try:
        is_id = False
        if 'Ideal' in type(I).__name__:
            is_id = True
        elif I in (S.Integers, S.Rationals, S.Reals, S.Complexes) and I == R:
            is_id = True
        else:
            I_set = set(I)
            if not I_set:
                is_id = False
            elif isinstance(R, (int, sympy.Integer)) and int(R) >= 2:
                n = int(R)
                is_all_ints = True
                for x in I_set:
                    if not isinstance(x, (int, sympy.Integer)):
                        is_all_ints = False
                        break
                if is_all_ints:
                    I_int = {int(x) for x in I_set}
                    if all(0 <= x < n for x in I_int):
                        is_id = True
                        # Check closure under subtraction
                        for x in I_int:
                            for y in I_int:
                                if (x - y) % n not in I_int:
                                    is_id = False
                                    break
                            if not is_id:
                                break
                        # Check closure under scalar multiplication
                        if is_id:
                            for x in I_int:
                                for r in range(n):
                                    if (r * x) % n not in I_int:
                                        is_id = False
                                        break
                                if not is_id:
                                    break
                    else:
                        is_id = False
                else:
                    is_id = False
            else:
                # For infinite rings like ZZ or QQ, a finite set is an ideal iff it is {0}
                if I_set == {0} or I_set == {0.0}:
                    is_id = True
                else:
                    is_id = False
        neg_q = not is_id
    except Exception:
        # If I cannot be converted to a set or evaluated, it is not a valid ideal.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: I is not the kernel of any surjective ring homomorphism from R (i.e. I is not an ideal of R)"
]

N_HYP = 1
NEG_Q_INDEX = 1