import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
import itertools
import functools
import math

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

def is_boolean_ring(R_add, R_mul):
    try:
        n = len(R_add)
        if n == 0: return False
        if len(R_mul) != n: return False
        for row in R_add + R_mul:
            if len(row) != n: return False
            for x in row:
                if not (isinstance(x, int) and 0 <= x < n): return False
                
        # Addition commutative
        for i in range(n):
            for j in range(n):
                if R_add[i][j] != R_add[j][i]: return False
                
        # Addition associative
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if R_add[R_add[i][j]][k] != R_add[i][R_add[j][k]]: return False
                    
        # Addition identity
        zero = None
        for i in range(n):
            if all(R_add[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None: return False
        
        # Addition inverse
        for i in range(n):
            if not any(R_add[i][j] == zero for j in range(n)): return False
            
        # Multiplication commutative
        for i in range(n):
            for j in range(n):
                if R_mul[i][j] != R_mul[j][i]: return False
                
        # Multiplication associative
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if R_mul[R_mul[i][j]][k] != R_mul[i][R_mul[j][k]]: return False
                    
        # Distributive
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if R_mul[i][R_add[j][k]] != R_add[R_mul[i][j]][R_mul[i][k]]: return False
                    
        # Boolean (x^2 = x)
        for i in range(n):
            if R_mul[i][i] != i: return False
            
        return True
    except Exception:
        return False

def is_fraction_ring_boolean(R_add, R_mul, S):
    try:
        n = len(R_add)
        if not S: return False 
        
        zero = next(i for i in range(n) if all(R_add[i][j] == j for j in range(n)))
        
        def sim(p1, p2):
            a, s = p1
            b, t = p2
            return any(R_mul[u][R_add[R_mul[a][t]][R_mul[b][s]]] == zero for u in S)
            
        pairs = [(a, s) for a in range(n) for s in S]
        num_pairs = len(pairs)
        
        sim_matrix = [[False]*num_pairs for _ in range(num_pairs)]
        for i in range(num_pairs):
            for j in range(num_pairs):
                sim_matrix[i][j] = sim(pairs[i], pairs[j])
                
        # Check equivalence relation
        for i in range(num_pairs):
            if not sim_matrix[i][i]: return False
            
        for i in range(num_pairs):
            for j in range(i+1, num_pairs):
                if sim_matrix[i][j] != sim_matrix[j][i]: return False
                
        for i in range(num_pairs):
            sim_i = sim_matrix[i]
            for j in range(num_pairs):
                if sim_i[j]:
                    sim_j = sim_matrix[j]
                    for k in range(num_pairs):
                        if sim_j[k] and not sim_i[k]: return False
                        
        # Form equivalence classes
        classes = []
        visited = [False]*num_pairs
        for i in range(num_pairs):
            if not visited[i]:
                c = []
                for j in range(num_pairs):
                    if sim_matrix[i][j]:
                        c.append(pairs[j])
                        visited[j] = True
                classes.append(c)
                
        m = len(classes)
        Q_add = [[0]*m for _ in range(m)]
        Q_mul = [[0]*m for _ in range(m)]
        
        def get_class_idx(p):
            for i, c in enumerate(classes):
                if p in c:
                    return i
            return -1
            
        for i in range(m):
            for j in range(m):
                a, s = classes[i][0]
                b, t = classes[j][0]
                
                st = R_mul[s][t]
                if st not in S: return False
                
                at = R_mul[a][t]
                bs = R_mul[b][s]
                sum_num = R_add[at][bs]
                sum_p = (sum_num, st)
                idx_add = get_class_idx(sum_p)
                if idx_add == -1: return False
                Q_add[i][j] = idx_add
                
                ab = R_mul[a][b]
                mul_p = (ab, st)
                idx_mul = get_class_idx(mul_p)
                if idx_mul == -1: return False
                Q_mul[i][j] = idx_mul
                
        return is_boolean_ring(Q_add, Q_mul)
    except Exception:
        return False

def conditions(witness):
    def extract_witness(w):
        if isinstance(w, tuple) and len(w) >= 3:
            return w[0], w[1], list(set(w[2]))
        elif hasattr(w, 'R_add') and hasattr(w, 'R_mul') and hasattr(w, 'S'):
            return w.R_add, w.R_mul, list(set(w.S))
        elif hasattr(w, 'elements') and hasattr(w, 'add') and hasattr(w, 'mul') and hasattr(w, 'S'):
            elements = list(w.elements)
            n = len(elements)
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            R_add = [[elem_to_idx[w.add(a, b)] for b in elements] for a in elements]
            R_mul = [[elem_to_idx[w.mul(a, b)] for b in elements] for a in elements]
            S = [elem_to_idx[s] for s in w.S]
            return R_add, R_mul, list(set(S))
        else:
            raise ValueError("Unknown witness format")

    try:
        R_add, R_mul, S = extract_witness(witness)
    except Exception:
        return [False, False, False]

    try:
        h1 = is_boolean_ring(R_add, R_mul)
    except Exception:
        h1 = False

    try:
        n = len(R_add)
        h2 = all(isinstance(s, int) and 0 <= s < n for s in S)
    except Exception:
        h2 = False

    try:
        if not h2:
            neg_q = False
        else:
            neg_q = not is_fraction_ring_boolean(R_add, R_mul, S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: S is a subset of R",
    "¬Q: S^{-1}R is not a Boolean ring"
]

N_HYP = 2
NEG_Q_INDEX = 2