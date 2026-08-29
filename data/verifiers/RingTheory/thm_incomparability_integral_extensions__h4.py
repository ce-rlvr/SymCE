import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

class Z2:
    def __init__(self, a):
        self.a = a % 2
    def __add__(self, other):
        return Z2(self.a + other.a)
    def __sub__(self, other):
        return Z2(self.a - other.a)
    def __mul__(self, other):
        return Z2(self.a * other.a)
    def __eq__(self, other):
        return isinstance(other, Z2) and self.a == other.a
    def __hash__(self):
        return hash(self.a)
    def __repr__(self):
        return f"Z2({self.a})"

class Z2_x:
    def __init__(self, a, b):
        self.a = a % 2
        self.b = b % 2
    def __add__(self, other):
        return Z2_x(self.a + other.a, self.b + other.b)
    def __sub__(self, other):
        return Z2_x(self.a - other.a, self.b - other.b)
    def __mul__(self, other):
        return Z2_x(self.a * other.a, self.a * other.b + self.b * other.a)
    def __eq__(self, other):
        return isinstance(other, Z2_x) and self.a == other.a and self.b == other.b
    def __hash__(self):
        return hash((self.a, self.b))
    def __repr__(self):
        return f"Z2_x({self.a}, {self.b})"

def is_comm_ring_with_id(ring):
    try:
        ring = list(ring)
    except Exception:
        return False
    if not ring or len(ring) > 100: 
        return False
    
    zeros = []
    for z in ring:
        if all(z + a == a and a + z == a for a in ring):
            zeros.append(z)
    if not zeros: 
        return False
    zero = zeros[0]
    
    ones = []
    for u in ring:
        if all(u * a == a and a * u == a for a in ring):
            ones.append(u)
    if not ones: 
        return False
    one = ones[0]
    
    for a in ring:
        if not any(a + b == zero for b in ring): 
            return False
        for b in ring:
            if (a + b) not in ring: return False
            if (a * b) not in ring: return False
            if a + b != b + a: return False
            if a * b != b * a: return False
            for c in ring:
                if (a + b) + c != a + (b + c): return False
                if (a * b) * c != a * (b * c): return False
                if a * (b + c) != (a * b) + (a * c): return False
    return True

def is_subring(R, S):
    try:
        R_list = list(R)
        S_list = list(S)
    except Exception:
        return False
    
    for r in R_list:
        if r not in S_list:
            return False
            
    ones_S = [u for u in S_list if all(u * a == a for a in S_list)]
    ones_R = [u for u in R_list if all(u * a == a for a in R_list)]
    if not ones_S or not ones_R: 
        return False
    if ones_S[0] != ones_R[0]: 
        return False
    
    return True

def is_integral_extension(R, S):
    try:
        R_list = list(R)
        S_list = list(S)
    except Exception:
        return False
        
    zeros = [z for z in S_list if all(z + a == a for a in S_list)]
    ones = [u for u in S_list if all(u * a == a for a in S_list)]
    if not zeros or not ones: 
        return False
    zero = zeros[0]
    one = ones[0]
    
    for s in S_list:
        found = False
        for deg in range(1, len(S_list) + 1):
            if len(R_list)**deg > 10000:
                break
            for coeffs in itertools.product(R_list, repeat=deg):
                val = one
                for _ in range(deg): 
                    val = val * s
                for i, c in enumerate(coeffs):
                    term = c
                    for _ in range(i): 
                        term = term * s
                    val = val + term
                if val == zero:
                    found = True
                    break
            if found:
                break
        if not found:
            return False
    return True

def conditions(witness):
    try:
        R, S, Q1, Q2 = witness
    except Exception:
        return [False] * 6
    
    try:
        h1 = is_comm_ring_with_id(R) and is_comm_ring_with_id(S)
    except Exception:
        h1 = False

    try:
        h2 = is_subring(R, S)
    except Exception:
        h2 = False

    try:
        h3 = is_integral_extension(R, S)
    except Exception:
        h3 = False

    try:
        h4 = set(Q1).issubset(set(Q2))
    except Exception:
        h4 = False

    try:
        h5 = set(Q1).intersection(set(R)) == set(Q2).intersection(set(R))
    except Exception:
        h5 = False

    try:
        neg_q = set(Q1) != set(Q2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: S is an integral extension of R",
    "H_4: Q_1 is a subset of Q_2",
    "H_5: Q_1 ∩ R = Q_2 ∩ R",
    "¬Q: Q_1 != Q_2"
]

N_HYP = 5
NEG_Q_INDEX = 5