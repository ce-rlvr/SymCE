import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            M = witness.get('M')
            F = witness.get('F')
        elif hasattr(witness, 'M') and hasattr(witness, 'F'):
            M = witness.M
            F = witness.F
        else:
            M, F = witness
    except Exception:
        return [False, False, False]
        
    # H1: M is an Artinian R-module
    # Finite sets, finite groups, and finite-dimensional matrices are Artinian.
    try:
        if isinstance(M, (list, set, tuple)):
            h1 = True
        elif hasattr(M, 'is_group') and M.is_group:
            h1 = True
        elif isinstance(M, Matrix):
            h1 = True
    except Exception:
        pass
        
    # H2: F is an arbitrary non-empty family of submodules of M
    try:
        if F and isinstance(F, (list, set, tuple)):
            h2 = True
            for sub in F:
                if isinstance(M, (list, set, tuple)):
                    if not set(sub).issubset(set(M)):
                        h2 = False
                        break
                elif hasattr(M, 'is_group'):
                    if not (hasattr(sub, 'is_group') and sub.is_subgroup(M)):
                        h2 = False
                        break
                elif isinstance(M, Matrix):
                    if not isinstance(sub, Matrix):
                        h2 = False
                        break
    except Exception:
        pass
        
    # ¬Q: There does NOT exist a finite subset of F such that the intersection
    # of the submodules in the finite subset is equal to the intersection of all submodules in F.
    try:
        if h2:
            # Since F is evaluated as a Python list/set/tuple, it is strictly finite.
            # Therefore, F itself is a finite subset of F.
            # The intersection of all submodules in F is trivially equal to 
            # the intersection of all submodules in this finite subset (which is F itself).
            # Thus, such a finite subset always exists, and the negation of the conclusion is False.
            # (Note: The theorem is actually true for all Artinian modules, so no valid counterexample exists).
            neg_q = False
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is an Artinian R-module",
    "H_2: F is an arbitrary non-empty family of submodules of M",
    "¬Q: There does not exist a finite subset of F with the same intersection as F"
]

N_HYP = 2
NEG_Q_INDEX = 2