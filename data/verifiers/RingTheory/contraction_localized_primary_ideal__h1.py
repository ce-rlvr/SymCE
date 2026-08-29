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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_subset(sub, sup):
    return all(x in sup for x in sub)

def are_equal(set1, set2):
    return is_subset(set1, set2) and is_subset(set2, set1)

def is_disjoint(set1, set2):
    return not any(x in set2 for x in set1)

def conditions(witness) -> list[bool]:
    # H1: S is a multiplicatively closed subset of R
    try:
        R = witness.elements
        S = witness.S
        if not R or not S or not is_subset(S, R):
            h1 = False
        else:
            h1 = True
            for a in S:
                for b in S:
                    if witness.mul(a, b) not in S:
                        h1 = False
                        break
                if not h1: break
    except Exception:
        h1 = False

    # H2: Q is a P-primary ideal of R
    try:
        R = witness.elements
        Q = witness.Q
        P = witness.P
        
        if not R or not Q or not P or not is_subset(Q, R) or not is_subset(P, R):
            h2 = False
        else:
            h2 = True
            
            # Basic closure of R
            if h2:
                for a in R:
                    for b in R:
                        if witness.add(a, b) not in R: h2 = False
                        if witness.mul(a, b) not in R: h2 = False
            
            # Q is ideal
            if h2:
                for a in Q:
                    for b in Q:
                        if witness.add(a, b) not in Q: h2 = False
            if h2:
                for r in R:
                    for q in Q:
                        if witness.mul(r, q) not in Q: h2 = False
                        if witness.mul(q, r) not in Q: h2 = False
            
            # P is ideal
            if h2:
                for a in P:
                    for b in P:
                        if witness.add(a, b) not in P: h2 = False
            if h2:
                for r in R:
                    for p in P:
                        if witness.mul(r, p) not in P: h2 = False
                        if witness.mul(p, r) not in P: h2 = False
                        
            if h2 and (are_equal(P, R) or are_equal(Q, R)):
                h2 = False
                
            # P is prime
            if h2:
                for a in R:
                    for b in R:
                        if all(witness.mul(a, witness.mul(r, b)) in P for r in R):
                            if a not in P and b not in P:
                                h2 = False
                                
            # Q is P-primary
            if h2:
                for a in R:
                    for b in R:
                        if all(witness.mul(a, witness.mul(r, b)) in Q for r in R):
                            if a not in Q and b not in P:
                                h2 = False
                                
            # P is radical of Q
            if h2:
                if not is_subset(Q, P):
                    h2 = False
                else:
                    current_prod = list(P)
                    for _ in range(len(R)):
                        if is_subset(current_prod, Q):
                            break
                        next_prod = []
                        for x in current_prod:
                            for y in P:
                                xy = witness.mul(x, y)
                                if xy not in next_prod:
                                    next_prod.append(xy)
                        current_prod = next_prod
                    else:
                        if not is_subset(current_prod, Q):
                            h2 = False
    except Exception:
        h2 = False

    # H3: The prime ideal P is disjoint from S
    try:
        S = witness.S
        P = witness.P
        if not S or not P:
            h3 = False
        else:
            h3 = is_disjoint(P, S)
    except Exception:
        h3 = False

    # Negated Conclusion: (S^{-1}Q)^c != Q
    try:
        R = witness.elements
        S = witness.S
        Q = witness.Q
        
        if not R or not S or not Q:
            neg_q = False
        else:
            left_contraction = []
            for x in R:
                for s in S:
                    if witness.mul(s, x) in Q:
                        if x not in left_contraction:
                            left_contraction.append(x)
                        break
                        
            right_contraction = []
            for x in R:
                for s in S:
                    if witness.mul(x, s) in Q:
                        if x not in right_contraction:
                            right_contraction.append(x)
                        break
                        
            neg_q = not are_equal(left_contraction, Q) or not are_equal(right_contraction, Q)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: Q is a P-primary ideal of R",
    "H_3: The prime ideal P is disjoint from S",
    "¬Q: The contraction of the extended ideal (S^{-1}Q)^c in R is not equal to Q"
]

N_HYP = 3
NEG_Q_INDEX = 3