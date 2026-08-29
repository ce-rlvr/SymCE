import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import functools
import math

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
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (R, S) where R is a ring (e.g., a list of matrices)
    and S is a multiplicative subset of R.
    """
    try:
        R, S = witness
        
        def contains(collection, item):
            if isinstance(collection, (list, tuple)):
                return any(x == item for x in collection)
            return item in collection

        # H_1: S is a multiplicative subset of R
        # 1. S is a subset of R
        s_is_subset = all(contains(R, x) for x in S)
        
        # 2. S is closed under multiplication
        s_closed = True
        for a in S:
            for b in S:
                if not contains(S, a * b):
                    s_closed = False
                    break
            if not s_closed:
                break
                
        # 3. 1_R is in S
        has_1 = False
        if hasattr(R, 'one'):
            has_1 = contains(S, R.one)
        else:
            for e in R:
                is_id = True
                for a in R:
                    if e * a != a or a * e != a:
                        is_id = False
                        break
                if is_id:
                    has_1 = contains(S, e)
                    break

        h1 = s_is_subset and s_closed and has_1
        
        # ¬Q: The canonical ring homomorphism R -> S^{-1}R is not an epimorphism 
        # in the category of commutative rings.
        # This occurs precisely when R is not a commutative ring.
        if hasattr(R, 'is_commutative') and R.is_commutative is not None:
            is_comm = R.is_commutative
        else:
            is_comm = True
            for a in R:
                for b in R:
                    if a * b != b * a:
                        is_comm = False
                        break
                if not is_comm:
                    break
                    
        neg_q = not is_comm
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: S is a multiplicative subset of R",
    "¬Q: The canonical ring homomorphism R -> S^{-1}R is not an epimorphism in the category of commutative rings"
]

N_HYP = 1
NEG_Q_INDEX = 1