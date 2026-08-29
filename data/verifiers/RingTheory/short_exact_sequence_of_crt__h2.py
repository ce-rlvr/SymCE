import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that I and J must be ideals of R.
    If they are not ideals, the quotients are not R-modules, and the sequence does not exist.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, I, J = witness
            elif len(witness) == 2:
                R = sympy.ZZ
                I, J = witness
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H1: R is a commutative ring
    h1 = False
    try:
        if hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        elif R in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
            h1 = True
        elif isinstance(R, set):
            h1 = True
    except Exception:
        pass

    # neg_Q: The sequence is NOT a short exact sequence of R-modules
    # This is True if I or J is not an ideal (so the R-modules are undefined).
    neg_q = False
    try:
        def is_ideal(S, R_obj):
            if hasattr(S, 'is_ideal') and S.is_ideal:
                return True
            if type(S).__name__ == 'Ideal':
                return True
            if isinstance(S, (int, sympy.Integer)):
                return True
            if isinstance(S, sympy.Expr) and not isinstance(S, (sympy.MatrixBase, set, list, tuple)):
                return True
            if isinstance(S, (set, frozenset, list, tuple)):
                S_list = list(S)
                if len(S_list) == 0:
                    return False
                
                has_zero = False
                for x in S_list:
                    try:
                        if x == 0 or (hasattr(R_obj, 'zero') and x == R_obj.zero):
                            has_zero = True
                            break
                    except Exception:
                        if x == 0:
                            has_zero = True
                            break
                if not has_zero:
                    return False
                
                for a in S_list:
                    for b in S_list:
                        try:
                            if (a + b) not in S_list:
                                return False
                        except Exception:
                            return False
                            
                if R_obj == sympy.ZZ:
                    if set(S_list) != {0}:
                        return False
                return True
            return False

        if not is_ideal(I, R) or not is_ideal(J, R):
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The sequence is not a short exact sequence of R-modules (e.g., I and J are not ideals)"
]

N_HYP = 1
NEG_Q_INDEX = 1