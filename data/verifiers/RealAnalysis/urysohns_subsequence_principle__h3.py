import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard mathematical objects
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H1: X is a topological space
    try:
        X = list(witness.X)
        topology = [set(u) for u in witness.topology]
        h1 = True
        
        # Check if empty set and X are in topology
        if set() not in topology or set(X) not in topology:
            h1 = False
            
        # Check closure under finite intersections
        if h1:
            for u in topology:
                for v in topology:
                    if u.intersection(v) not in topology:
                        h1 = False
                        break
                if not h1:
                    break
                    
        # Check closure under arbitrary unions (for finite spaces, pairwise is sufficient)
        if h1:
            for u in topology:
                for v in topology:
                    if u.union(v) not in topology:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: (x_n) is a sequence in X
    try:
        if hasattr(witness, 'pre_period') and hasattr(witness, 'period'):
            pre_period = list(witness.pre_period)
            period = list(witness.period)
        elif hasattr(witness, 'seq'):
            if callable(witness.seq):
                vals = [witness.seq(n) for n in range(100)]
                pre_period = vals[:50]
                period = list(set(vals[50:]))
            else:
                pre_period = []
                period = list(witness.seq)
        else:
            raise ValueError
        
        h2 = True
        if not period:
            h2 = False
        for x in pre_period + period:
            if x not in X:
                h2 = False
                break
    except Exception:
        h2 = False

    # H3: Every subsequence of (x_n) contains a further subsequence that converges to L
    try:
        L = witness.L
        if L not in X:
            h3 = False
        else:
            h3 = True
            # For an eventually periodic sequence in a finite space, every subsequence has a 
            # further subsequence converging to L iff every element in the period converges to L.
            for c in period:
                for u in topology:
                    if L in u and c not in u:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # neg_Q: The sequence (x_n) does not converge to L
    try:
        L = witness.L
        h4 = True
        # The sequence converges to L iff it is eventually in every open set containing L.
        # For an eventually periodic sequence, this means all elements in the period 
        # must be in every open set containing L.
        for u in topology:
            if L in u:
                for c in period:
                    if c not in u:
                        h4 = False
                        break
            if not h4:
                break
        neg_q = not h4
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: (x_n) is a sequence in X",
    "H_3: Every subsequence of (x_n) contains a further subsequence that converges to L",
    "¬Q: The sequence (x_n) does not converge to L"
]

N_HYP = 3
NEG_Q_INDEX = 3