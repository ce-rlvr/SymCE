import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            if 'is_separable' in witness:
                h1 = bool(witness['is_separable'])
            if 'is_pointwise_bounded' in witness:
                h2 = bool(witness['is_pointwise_bounded'])
            if 'has_convergent_subsequence_on_dense_subset' in witness:
                neg_q = not bool(witness['has_convergent_subsequence_on_dense_subset'])
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_separable'):
            h1 = bool(witness.is_separable)
        if hasattr(witness, 'is_pointwise_bounded'):
            h2 = bool(witness.is_pointwise_bounded)
        if hasattr(witness, 'has_convergent_subsequence_on_dense_subset'):
            neg_q = not bool(witness.has_convergent_subsequence_on_dense_subset)
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            X, f = witness
            if isinstance(X, (list, tuple)):
                h1 = True
                
                bounded = True
                for x in X:
                    vals = []
                    for n in range(1, 100):
                        try:
                            vals.append(float(f(n, x)))
                        except Exception:
                            pass
                    if len(vals) > 0 and (max(vals) - min(vals) > 1e6):
                        bounded = False
                h2 = bounded
                
                neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a separable metric space",
    "H_2: For every x in X, the sequence of real numbers {f_n(x)} is bounded",
    "¬Q: The sequence {f_n} does not contain a subsequence that converges pointwise on a countable dense subset of X"
]

N_HYP = 2
NEG_Q_INDEX = 2