import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy import ZZ, QQ, eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_unit(d, R):
    if d == 1 or d == -1:
        return True
    if hasattr(R, 'is_unit'):
        try:
            return bool(R.is_unit(d))
        except Exception:
            pass
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (R, M, N) where:
      - R is a sympy domain (e.g., ZZ) or the string 'ZZ'.
      - M and N represent R-modules. They can be:
          * An integer k >= 0, representing the free module R^k.
          * A list/tuple of elements in R, representing the invariant factors of the module.
          * A sympy PermutationGroup (only valid if R is ZZ), representing a finite abelian group.
    """
    try:
        R, M, N = witness
    except Exception:
        return [False, False, False]
    
    # H1: R is a principal ideal domain
    try:
        if R == 'ZZ' or R == ZZ:
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: M is a cyclic R-module
    try:
        h2 = False
        if h1:
            if (R == 'ZZ' or R == ZZ) and hasattr(M, 'is_abelian') and M.is_abelian:
                h2 = bool(M.is_cyclic)
            elif isinstance(M, int) and M >= 0:
                h2 = (M <= 1)
            elif isinstance(M, (list, tuple)):
                non_units = [d for d in M if not is_unit(d, R)]
                h2 = (len(non_units) <= 1)
    except Exception:
        h2 = False

    # neg_Q: N is NOT a cyclic R-module
    try:
        neg_q = False
        if h1:
            if (R == 'ZZ' or R == ZZ) and hasattr(N, 'is_abelian') and N.is_abelian:
                neg_q = not bool(N.is_cyclic)
            elif isinstance(N, int) and N >= 0:
                neg_q = (N > 1)
            elif isinstance(N, (list, tuple)):
                non_units = [d for d in N if not is_unit(d, R)]
                neg_q = (len(non_units) > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a cyclic R-module",
    "¬Q: N is not a cyclic R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2