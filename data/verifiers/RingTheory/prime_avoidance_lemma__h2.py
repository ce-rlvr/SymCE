import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def get_op(op):
    if callable(op):
        return op
    elif isinstance(op, (list, tuple)):
        return lambda a, b: op[a][b]
    elif isinstance(op, dict):
        return lambda a, b: op[(a, b)]
    else:
        raise ValueError("Operator must be callable, list, or dict")

def conditions(witness):
    try:
        R_raw, add_op, mul_op, I, P_list = witness
        
        R = []
        for i, x in enumerate(R_raw):
            if i > 200:
                raise ValueError("Ring too large")
            R.append(x)
            
        add = get_op(add_op)
        mul = get_op(mul_op)
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring
    h1 = True
    zero = None
    try:
        if not R: 
            h1 = False
        else:
            # Check closure, commutativity, associativity of add
            for a in R:
                for b in R:
                    ab = add(a, b)
                    if ab not in R: h1 = False
                    if ab != add(b, a): h1 = False
                    for c in R:
                        if add(ab, c) != add(a, add(b, c)): h1 = False
            
            if h1:
                zeros_list = [z for z in R if all(add(z, a) == a for a in R)]
                if not zeros_list: 
                    h1 = False
                else:
                    zero = zeros_list[0]
            
            if h1:
                for a in R:
                    if not any(add(a, b) == zero for b in R): h1 = False
                    
            # Check closure, commutativity, associativity of mul
            if h1:
                for a in R:
                    for b in R:
                        ab = mul(a, b)
                        if ab not in R: h1 = False
                        if ab != mul(b, a): h1 = False
                        for c in R:
                            if mul(ab, c) != mul(a, mul(b, c)): h1 = False
                            
            # Check distributivity
            if h1:
                for a in R:
                    for b in R:
                        for c in R:
                            if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1 = False
                            
            # Check for multiplicative identity (1)
            if h1:
                has_one = False
                for e in R:
                    if all(mul(e, a) == a for a in R):
                        has_one = True
                        break
                if not has_one:
                    h1 = False
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    h2 = True
    try:
        if not h1:
            h2 = False
        else:
            I_set = set(I)
            if not I_set.issubset(set(R)): h2 = False
            if zero not in I_set: h2 = False
            for a in I_set:
                for b in I_set:
                    if add(a, b) not in I_set: h2 = False
                has_inv = False
                for b in I_set:
                    if add(a, b) == zero:
                        has_inv = True
                        break
                if not has_inv: h2 = False
            for r in R:
                for a in I_set:
                    if mul(r, a) not in I_set: h2 = False
    except Exception:
        h2 = False

    # H3: I \subseteq \bigcup P_i and P_i are ideals
    h3 = True
    try:
        if not h1:
            h3 = False
        else:
            union_P = set()
            for P in P_list:
                P_set = set(P)
                if not P_set.issubset(set(R)): h3 = False
                if zero not in P_set: h3 = False
                for a in P_set:
                    for b in P_set:
                        if add(a, b) not in P_set: h3 = False
                    has_inv = False
                    for b in P_set:
                        if add(a, b) == zero:
                            has_inv = True
                            break
                    if not has_inv: h3 = False
                for r in R:
                    for a in P_set:
                        if mul(r, a) not in P_set: h3 = False
                union_P.update(P_set)
            
            for x in I:
                if x not in union_P:
                    h3 = False
    except Exception:
        h3 = False

    # neg_Q: I \not\subseteq P_i for all i
    neg_q = True
    try:
        I_set = set(I)
        for P in P_list:
            if I_set.issubset(set(P)):
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: P_i are ideals and I is contained in their union",
    "¬Q: I is not contained in any P_i"
]

N_HYP = 3
NEG_Q_INDEX = 3