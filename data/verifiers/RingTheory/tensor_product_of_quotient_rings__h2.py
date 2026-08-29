import sympy
import sympy.combinatorics
import sympy.matrices

# Top-level setup for potential witness elements
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
    "H_2: J is an ideal of R",
    "¬Q: The tensor product (R/I) \\otimes_R (R/J) is not isomorphic to R/(I+J)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
        else:
            R = witness.R
            I = witness.I
            J = witness.J
    except Exception:
        try:
            R, I, J = witness
        except Exception:
            return [False, False, False]

    def check_commutative_ring(R):
        if hasattr(R, 'is_commutative_ring'):
            if callable(R.is_commutative_ring):
                return R.is_commutative_ring()
            return R.is_commutative_ring
        if R in (sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC, 
                 sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            return True
        if hasattr(R, 'is_commutative'):
            if not R.is_commutative:
                return False
            if hasattr(R, 'is_ring') and R.is_ring:
                return True
        return False

    def check_ideal(X, R):
        if X is not False and X is not True:
            if X == 0 or X == R:
                return True
        if hasattr(X, 'is_ideal_of'):
            try:
                if X.is_ideal_of(R):
                    return True
            except Exception:
                pass
        if R == sympy.ZZ or R == sympy.S.Integers:
            if isinstance(X, (int, sympy.Integer)):
                return True
            if X == sympy.S.Integers or X == sympy.ZZ:
                return True
            if hasattr(sympy, 'ImageSet') and isinstance(X, sympy.ImageSet):
                if X.base_set == sympy.S.Integers:
                    return True
            return False
        if R in (sympy.QQ, sympy.RR, sympy.CC, 
                 sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            if X == 0 or X == R:
                return True
            return False
        return False

    try:
        h1 = bool(check_commutative_ring(R))
    except Exception:
        h1 = False

    try:
        h2 = bool(check_ideal(J, R))
    except Exception:
        h2 = False

    try:
        # The theorem holds for all commutative rings when both I and J are ideals.
        # The conclusion fails (is undefined/not isomorphic) iff I is not an ideal.
        neg_q = not check_ideal(I, R)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]