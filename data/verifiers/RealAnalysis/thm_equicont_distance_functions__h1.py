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

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def check_H1(witness):
    """
    Check if \mathcal{A} is an arbitrary family of non-empty subsets of X.
    """
    try:
        A_family = witness.A_family
        X = getattr(witness, 'X', None)
        
        for A in A_family:
            # Check non-empty
            if hasattr(A, 'is_empty'):
                if A.is_empty:
                    return False
            else:
                try:
                    iterator = iter(A)
                    next(iterator)
                except StopIteration:
                    return False
                except TypeError:
                    return False
            
            # Check subset of X
            if X is not None:
                if hasattr(X, '__contains__'):
                    try:
                        for a in A:
                            if a not in X:
                                return False
                    except TypeError:
                        if hasattr(A, 'is_subset'):
                            if not A.is_subset(X):
                                return False
        return True
    except Exception:
        return False

def check_neg_Q(witness):
    """
    Check if the family of distance functions is NOT uniformly equicontinuous on X.
    """
    try:
        epsilon = float(getattr(witness, 'epsilon', 1.0))
        if epsilon <= 0:
            return False
            
        d = witness.d
        d_X = getattr(witness, 'd_X', d)
        
        def f_A(A, x):
            if hasattr(witness, 'f'):
                return witness.f(A, x)
            else:
                return min(d(x, a) for a in A)
        
        deltas = [1.0, 0.1, 0.01, 0.001, 1e-4, 1e-5]
        
        if hasattr(witness, 'get_counterexample'):
            for delta in deltas:
                A, x, y = witness.get_counterexample(delta)
                if float(d_X(x, y)) >= delta:
                    return False
                
                val_x = float(f_A(A, x))
                val_y = float(f_A(A, y))
                
                if math.isinf(val_x) and math.isinf(val_y) and (val_x == val_y):
                    diff = float('nan')
                else:
                    diff = abs(val_x - val_y)
                    
                if math.isnan(diff):
                    continue
                if diff < epsilon:
                    return False
            return True
            
        elif hasattr(witness, 'counterexamples'):
            for delta, A, x, y in witness.counterexamples:
                if float(d_X(x, y)) >= delta:
                    return False
                
                val_x = float(f_A(A, x))
                val_y = float(f_A(A, y))
                
                if math.isinf(val_x) and math.isinf(val_y) and (val_x == val_y):
                    diff = float('nan')
                else:
                    diff = abs(val_x - val_y)
                    
                if math.isnan(diff):
                    continue
                if diff < epsilon:
                    return False
            return True
            
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    return [check_H1(witness), check_neg_Q(witness)]

CONDITION_LABELS = [
    "H_1: \\mathcal{A} is an arbitrary family of non-empty subsets of X",
    "¬Q: The family of distance functions is NOT uniformly equicontinuous on X"
]

N_HYP = 1
NEG_Q_INDEX = 1