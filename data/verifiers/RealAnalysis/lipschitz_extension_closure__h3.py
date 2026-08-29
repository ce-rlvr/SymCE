import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy import S, diff, limit, oo, Abs

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

def conditions(witness):
    try:
        X, A, f, x_sym = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = X.is_subset(S.Reals)
    except Exception:
        h1 = False
        
    try:
        h2 = A.is_subset(X) and X.is_subset(A.closure)
    except Exception:
        h2 = False
        
    try:
        df = diff(f, x_sym)
        is_lip = True
        
        try:
            boundary = A.closure - A.interior
            if boundary.is_FiniteSet:
                for pt in boundary:
                    if pt.is_real:
                        lim = limit(Abs(df), x_sym, pt)
                        if lim in [oo, -oo, sympy.zoo]:
                            is_lip = False
                            break
        except Exception:
            pass
            
        try:
            if A.sup == oo:
                lim = limit(Abs(df), x_sym, oo)
                if lim in [oo, -oo, sympy.zoo]:
                    is_lip = False
        except Exception:
            pass
            
        try:
            if A.inf == -oo:
                lim = limit(Abs(df), x_sym, -oo)
                if lim in [oo, -oo, sympy.zoo]:
                    is_lip = False
        except Exception:
            pass
            
        neg_q = not is_lip
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: A is a dense subset of X",
    "¬Q: f cannot be extended to a Lipschitz continuous function on X with the same Lipschitz constant"
]

N_HYP = 2
NEG_Q_INDEX = 2