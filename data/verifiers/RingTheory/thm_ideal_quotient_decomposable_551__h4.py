import math
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def is_primary(q):
    q = abs(q)
    if q == 0:
        return True
    if q == 1:
        return False
    factors = factorint(q)
    return len(factors) == 1

def intersect_ideals(ideals):
    if not ideals:
        return 1
    res = ideals[0]
    for a in ideals[1:]:
        res = math.lcm(res, a)
    return res

def ideal_quotient(A, B):
    if isinstance(B, (list, set)):
        if not B:
            return 1
        b_gen = 0
        for b in B:
            b_gen = math.gcd(b_gen, abs(b))
        B = b_gen
    else:
        B = abs(B)
        
    A = abs(A)
    if B == 0:
        return 1
    if A == 0:
        return 0
    return A // math.gcd(A, B)

def is_ideal(n, subset):
    if not isinstance(subset, (list, set)):
        return False
    if not subset:
        return False
    subset = set(x % n for x in subset)
    if 0 not in subset:
        return False
    for a in subset:
        for b in subset:
            if (a + b) % n not in subset:
                return False
    for a in subset:
        for r in range(n):
            if (a * r) % n not in subset:
                return False
    return True

def is_primary_zn(n, Q):
    Q = set(x % n for x in Q)
    if len(Q) == n: 
        return False
    for a in range(n):
        for b in range(n):
            if (a * b) % n in Q:
                if a not in Q:
                    bk = b % n
                    found = False
                    for k in range(1, n + 2):
                        if bk in Q:
                            found = True
                            break
                        bk = (bk * b) % n
                    if not found:
                        return False
    return True

def ideal_quotient_zn(n, A, B):
    A = set(x % n for x in A)
    B = set(x % n for x in B)
    res = set()
    for x in range(n):
        if all((x * b) % n in A for b in B):
            res.add(x)
    return res

def ideal_intersection(n, ideals):
    if not ideals:
        return set(range(n))
    res = set(range(n))
    for idl in ideals:
        res = res.intersection(set(x % n for x in idl))
    return res

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    Expected witness formats:
      - For Z: ('Z', I, Q_list, J) where I, J are ints (or J is list of ints), Q_list is list of ints.
      - For Z/nZ: ('Zn', n, I, Q_list, J) where n is int, I, J are lists of ints, Q_list is list of lists of ints.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) < 4:
            return [False, False, False, False]
            
        ring_type = witness[0]
        
        if ring_type == 'Z':
            _, I, Q_list, J = witness
            
            # H_1: R is a commutative ring
            h1 = True
            
            # H_2: I is an ideal in R
            h2 = isinstance(I, int)
            
            # H_3: I has a primary decomposition I = \bigcap_{i=1}^n Q_i
            h3 = False
            if isinstance(Q_list, list) and all(isinstance(q, int) for q in Q_list):
                if intersect_ideals(Q_list) == abs(I):
                    if all(is_primary(abs(q)) for q in Q_list):
                        h3 = True
                        
            # ¬Q: The ideal quotient (I:J) is NOT equal to the intersection \bigcap_{i=1}^n (Q_i:J)
            if isinstance(J, (int, list, set)):
                I_colon_J = ideal_quotient(I, J)
                Q_colon_J_list = [ideal_quotient(q, J) for q in Q_list]
                intersect_Q_colon_J = intersect_ideals(Q_colon_J_list)
                neg_q = (I_colon_J != intersect_Q_colon_J)
            else:
                neg_q = False
                
            return [h1, h2, h3, neg_q]
            
        elif ring_type == 'Zn':
            _, n, I, Q_list, J = witness
            
            # H_1: R is a commutative ring
            h1 = isinstance(n, int) and n >= 2
            
            # H_2: I is an ideal in R
            h2 = is_ideal(n, I)
            
            # H_3: I has a primary decomposition I = \bigcap_{i=1}^n Q_i
            h3 = False
            if isinstance(Q_list, list) and all(is_ideal(n, q) for q in Q_list):
                if ideal_intersection(n, Q_list) == set(x % n for x in I):
                    if all(is_primary_zn(n, q) for q in Q_list):
                        h3 = True
                        
            # ¬Q: The ideal quotient (I:J) is NOT equal to the intersection \bigcap_{i=1}^n (Q_i:J)
            if isinstance(J, (list, set)):
                I_colon_J = ideal_quotient_zn(n, I, J)
                Q_colon_J_list = [ideal_quotient_zn(n, q, J) for q in Q_list]
                intersect_Q_colon_J = ideal_intersection(n, Q_colon_J_list)
                neg_q = (I_colon_J != intersect_Q_colon_J)
            else:
                neg_q = False
                
            return [h1, h2, h3, neg_q]
            
        else:
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal in R",
    "H_3: I has a primary decomposition I = \\bigcap_{i=1}^n Q_i",
    "¬Q: The ideal quotient (I:J) is NOT equal to the intersection \\bigcap_{i=1}^n (Q_i:J)"
]

N_HYP = 3
NEG_Q_INDEX = 3