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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        R = list(witness.R)
        zero = witness.zero
        add = witness.add
        mul = witness.mul
        d = witness.d
        a = witness.a
        b = witness.b
        
        sub_dict = {}
        for i in R:
            for j in R:
                sub_dict[(add(i, j), i)] = j
                
        def sub(x, y):
            return sub_dict[(x, y)]
            
        # H1: d is a submultiplicative Euclidean function on R
        h1 = True
        for x in R:
            for y in R:
                if y == zero: continue
                found = False
                for q in R:
                    qy = mul(q, y)
                    r = sub(x, qy)
                    if r == zero or d(r) < d(y):
                        found = True
                        break
                if not found:
                    h1 = False
                    break
            if not h1: break
            
        if h1:
            for x in R:
                for y in R:
                    xy = mul(x, y)
                    if xy != zero and x != zero and y != zero:
                        if d(xy) > d(x) * d(y):
                            h1 = False
                            break
                if not h1: break
                
        # H2: a and b are non-zero elements of R
        h2 = (a in R) and (b in R) and (a != zero) and (b != zero)
        
        # H3: a divides b
        h3 = False
        if h2:
            for q in R:
                if mul(a, q) == b:
                    h3 = True
                    break
                    
        # H4: d(a) = d(b)
        h4 = False
        if h2:
            h4 = (d(a) == d(b))
            
        # neg_Q: a and b are not associate elements in R
        b_divides_a = False
        if h2:
            for q in R:
                if mul(b, q) == a:
                    b_divides_a = True
                    break
        
        neg_q = not (h3 and b_divides_a)
        
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: d is a submultiplicative Euclidean function on R",
    "H_2: a and b are non-zero elements of R",
    "H_3: a divides b",
    "H_4: d(a) = d(b)",
    "¬Q: a and b are not associate elements in R"
]

N_HYP = 4
NEG_Q_INDEX = 4