import math
import itertools
import functools
import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *

# Top-level setup for potential witness expressions
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
    try:
        X = witness['X']
        d = witness['d']
        seq = witness['seq']
    except Exception:
        return [False, False, False]

    h1 = False
    h2 = False
    try:
        X_list = []
        # Limit the size of X to prevent hanging on infinite iterables
        for i, x in enumerate(X):
            if i > 50:
                break
            X_list.append(x)
            
        if len(X_list) > 0 and len(X_list) <= 50:
            h1 = True
            h2 = True  # A finite set is always totally bounded
            
            # Check metric properties
            for x in X_list:
                for y in X_list:
                    dist = float(d(x, y))
                    if math.isnan(dist) or dist < -1e-7:
                        h1 = False
                        break
                    if x == y and dist > 1e-7:
                        h1 = False
                        break
                    if x != y and dist < 1e-7:
                        h1 = False
                        break
                    dyx = float(d(y, x))
                    if math.isnan(dyx) or abs(dist - dyx) > 1e-7:
                        h1 = False
                        break
                if not h1:
                    break
                    
            # Check triangle inequality
            if h1:
                for x in X_list:
                    for y in X_list:
                        d_xy = float(d(x, y))
                        for z in X_list:
                            d_xz = float(d(x, z))
                            d_yz = float(d(y, z))
                            if math.isnan(d_xz) or math.isnan(d_yz) or d_xz > d_xy + d_yz + 1e-7:
                                h1 = False
                                break
                        if not h1:
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False
        h2 = False

    neg_q = False
    try:
        # Generate the first 500 terms of the sequence
        if callable(seq):
            seq_vals = [seq(i) for i in range(1, 501)]
        else:
            seq_vals = list(itertools.islice(seq, 500))
            
        if len(seq_vals) == 500:
            min_dist = float('inf')
            # If the sequence has a Cauchy subsequence, the minimum distance 
            # between some distinct elements will be arbitrarily small.
            # If it is bounded away from 0, it cannot have a Cauchy subsequence.
            for i in range(len(seq_vals)):
                for j in range(i + 1, len(seq_vals)):
                    dist = float(d(seq_vals[i], seq_vals[j]))
                    if math.isnan(dist):
                        raise ValueError("Distance is NaN")
                    if dist < min_dist:
                        min_dist = dist
                    if min_dist <= 0.001:
                        break
                if min_dist <= 0.001:
                    break
            
            if min_dist > 0.001:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: X is totally bounded",
    "¬Q: The sequence (x_n) does not contain a Cauchy subsequence"
]

N_HYP = 2
NEG_Q_INDEX = 2