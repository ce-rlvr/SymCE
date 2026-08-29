import sympy
from sympy import Matrix, zeros, eye
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be a subset W of a finite-dimensional inner product space V.
        # We represent V as R^n, and W as a finite collection of column vectors (sympy.Matrix).
        if isinstance(witness, Matrix):
            # If a single Matrix is provided, treat its columns as the set of vectors W
            if witness.shape[1] == 1:
                witness_iterable = [witness]
            else:
                witness_iterable = [witness[:, i] for i in range(witness.shape[1])]
        elif isinstance(witness, (list, tuple, set)):
            witness_iterable = witness
        else:
            return [False, False]
            
        witness_list = []
        for v in witness_iterable:
            try:
                mat_v = Matrix(v)
                # Ensure all elements are column vectors
                if mat_v.shape[1] != 1:
                    if mat_v.shape[0] == 1:
                        mat_v = mat_v.T
                    else:
                        return [False, False]
                witness_list.append(mat_v)
            except Exception:
                return [False, False]
                
        if len(witness_list) == 0:
            return [False, False]
            
        n = witness_list[0].shape[0]
        for v in witness_list:
            if v.shape[0] != n:
                return [False, False]
                
        # H_1: V is a finite-dimensional inner product space
        # Since W is a set of vectors in R^n, V = R^n is a finite-dimensional inner product space.
        h1 = True
        
        # ¬Q: (W^\perp)^\perp \neq W
        # By standard linear algebra, (W^\perp)^\perp = span(W).
        # Since W is a finite set of vectors, W == span(W) if and only if W is the zero subspace {0}.
        # Thus, W is equal to its span iff it contains the zero vector and is closed under scalar multiplication.
        is_subspace = True
        zero_vec = zeros(n, 1)
        
        if zero_vec not in witness_list:
            is_subspace = False
        else:
            for v in witness_list:
                # Check closure under scalar multiplication (using scalar 2)
                if (2 * v) not in witness_list:
                    is_subspace = False
                    break
                    
        neg_q = not is_subspace
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "¬Q: (W^\\perp)^\\perp \\neq W"
]

N_HYP = 1
NEG_Q_INDEX = 1