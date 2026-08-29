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

def conditions(witness):
    try:
        R_iter, N_iter, x = witness
        R = list(R_iter)
        N = list(N_iter)
    except Exception:
        return [False, False, False]

    def check_h1():
        try:
            # Check if N is a subset of R
            for n in N:
                if n not in R: 
                    return False
            
            # Check if N is closed under addition and subtraction
            for n1 in N:
                for n2 in N:
                    if (n1 + n2) not in N: 
                        return False
                    if (n1 - n2) not in N: 
                        return False
            
            # Check if N is an ideal (absorbs multiplication from R)
            for n in N:
                for r in R:
                    if (n * r) not in N: 
                        return False
                    if (r * n) not in N: 
                        return False
            
            # Check if every element of N is nilpotent
            for n in N:
                is_nil = False
                curr = n
                for _ in range(len(R) + 5):
                    # curr + curr == curr is a robust check for the zero element
                    if curr + curr == curr:
                        is_nil = True
                        break
                    curr = curr * n
                if not is_nil: 
                    return False
                    
            return True
        except Exception:
            return False

    def check_h2():
        try:
            if x not in R: 
                return False
            if (x * x - x) not in N: 
                return False
            return True
        except Exception:
            return False

    def check_neg_q():
        try:
            for e in R:
                if e * e == e:
                    if (e - x) in N:
                        return False
            return True
        except Exception:
            return False

    h1 = check_h1()
    h2 = check_h2()
    neg_q = check_neg_q()

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is an ideal of R such that every element of N is nilpotent",
    "H_2: x is an element of R such that x^2 - x is in N",
    "¬Q: There does NOT exist an idempotent element e in R such that e - x is in N"
]

N_HYP = 2
NEG_Q_INDEX = 2