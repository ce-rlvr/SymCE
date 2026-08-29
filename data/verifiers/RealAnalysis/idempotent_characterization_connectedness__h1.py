import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    try:
        h1 = True
        
        # Try to parse witness as a topological space (X, T)
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, set, tuple)):
            X, T = witness
            n = len(X)
            X_set = set(X)
            T_sets = [set(u) for u in T]
            clopen_count = 0
            for u in T_sets:
                comp = X_set - u
                if comp in T_sets:
                    clopen_count += 1
        else:
            # Assume witness is n, or a collection of n points with discrete topology
            if isinstance(witness, int):
                n = witness
            elif hasattr(witness, '__len__'):
                n = len(witness)
            else:
                n = int(witness)
                
            if n < 0:
                return [False, False]
                
            clopen_count = 2**n
            
        # LHS: X is connected. A space is connected iff it has exactly 2 clopen sets.
        lhs = (clopen_count == 2)
        
        # RHS: The only idempotents in C(X, R) are 0 and 1.
        # Idempotents correspond to clopen sets.
        # The constant functions 0 and 1 correspond to the empty set and X.
        # If n == 0, empty set and X are the same, so there is 1 constant function.
        # If n > 0, they are distinct, so there are 2 constant functions.
        rhs = (clopen_count == (1 if n == 0 else 2))
        
        q = (lhs == rhs)
        neg_q = not q
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: C(X, R) is the ring of continuous real-valued functions on X",
    "¬Q: The equivalence between connectedness and trivial idempotents fails"
]

N_HYP = 1
NEG_Q_INDEX = 1