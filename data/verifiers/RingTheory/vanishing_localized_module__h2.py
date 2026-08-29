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

def extract(witness, name):
    if isinstance(witness, dict):
        return witness[name]
    return getattr(witness, name)

def get_sub_M(witness):
    try:
        return extract(witness, 'sub_M')
    except Exception:
        add_M = extract(witness, 'add_M')
        neg_M = extract(witness, 'neg_M')
        return lambda x, y: add_M(x, neg_M(y))

def check_H1(witness):
    try:
        R = extract(witness, 'R')
        add_R = extract(witness, 'add_R')
        mul_R = extract(witness, 'mul_R')
        zero_R = extract(witness, 'zero_R')
        
        if zero_R not in R: 
            return False
        
        for a in R:
            if add_R(a, zero_R) != a: return False
            if add_R(zero_R, a) != a: return False
            
            has_inv = False
            for b in R:
                if add_R(a, b) == zero_R and add_R(b, a) == zero_R:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in R:
                if add_R(a, b) not in R: return False
                if add_R(a, b) != add_R(b, a): return False
                if mul_R(a, b) not in R: return False
                if mul_R(a, b) != mul_R(b, a): return False
                
                for c in R:
                    if add_R(add_R(a, b), c) != add_R(a, add_R(b, c)): return False
                    if mul_R(mul_R(a, b), c) != mul_R(a, mul_R(b, c)): return False
                    if mul_R(a, add_R(b, c)) != add_R(mul_R(a, b), mul_R(a, c)): return False
                    
        has_one = False
        for e in R:
            is_one = True
            for a in R:
                if mul_R(e, a) != a or mul_R(a, e) != a:
                    is_one = False
                    break
            if is_one:
                has_one = True
                break
        if not has_one: return False
        
        return True
    except Exception:
        return False

def check_H2(witness):
    try:
        R = extract(witness, 'R')
        S = extract(witness, 'S')
        mul_R = extract(witness, 'mul_R')
        
        for s in S:
            if s not in R: return False
            for t in S:
                if mul_R(s, t) not in S: return False
        return True
    except Exception:
        return False

def check_Q(witness):
    try:
        S = extract(witness, 'S')
        M = extract(witness, 'M')
        mul_RM = extract(witness, 'mul_RM')
        zero_M = extract(witness, 'zero_M')
        sub_M = get_sub_M(witness)
        
        MxS = [(m, s) for m in M for s in S]
        if not MxS:
            lhs = False
        else:
            n = len(MxS)
            visited = [False] * n
            visited[0] = True
            q = [0]
            count = 1
            
            for curr in q:
                m1, s1 = MxS[curr]
                for j in range(n):
                    if not visited[j]:
                        m2, s2 = MxS[j]
                        rel = False
                        try:
                            diff1 = sub_M(mul_RM(s2, m1), mul_RM(s1, m2))
                            for t in S:
                                if mul_RM(t, diff1) == zero_M:
                                    rel = True
                                    break
                        except Exception:
                            pass
                        
                        if not rel:
                            try:
                                diff2 = sub_M(mul_RM(s1, m2), mul_RM(s2, m1))
                                for t in S:
                                    if mul_RM(t, diff2) == zero_M:
                                        rel = True
                                        break
                            except Exception:
                                pass
                                
                        if rel:
                            visited[j] = True
                            q.append(j)
                            count += 1
                            
            lhs = (count == n)
            
        rhs = True
        for m in M:
            found = False
            for s in S:
                try:
                    if mul_RM(s, m) == zero_M:
                        found = True
                        break
                except Exception:
                    pass
            if not found:
                rhs = False
                break
                
        return not (lhs == rhs)
    except Exception:
        return False

def conditions(witness):
    return [check_H1(witness), check_H2(witness), check_Q(witness)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}M = 0 is not equivalent to (for all m in M, exists s in S such that sm = 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2