import math
from itertools import combinations
import sympy
from sympy import Matrix

# Top-level setup: named object bindings that the witness expression may reference.
# A presentation is represented as a tuple (n, rels), where n is the number of generators
# and rels is a list of relations. Each relation is a list of non-zero integers in [-n, n].
# For example, 1 represents the first generator, -1 represents its inverse.
P_trivial = (0, [])
P_Z = (1, [])
P_Z2 = (1, [[1, 1]])
P_Z3 = (1, [[1, 1, 1]])
P_Z4 = (1, [[1, 1, 1, 1]])
P_Z2xZ2 = (2, [[1, 1], [2, 2], [1, 2, -1, -2]])
P_S3 = (2, [[1, 1], [2, 2, 2], [1, 2, 1, 2]])

def is_valid_presentation(P):
    if not isinstance(P, (tuple, list)) or len(P) != 2:
        return False
    n, rels = P
    if type(n) is not int or n < 0 or n > 10:
        return False
    if not isinstance(rels, (list, tuple)) or len(rels) > 20:
        return False
    for rel in rels:
        if not isinstance(rel, (list, tuple)) or len(rel) > 50:
            return False
        for x in rel:
            if type(x) is not int or x == 0 or abs(x) > n:
                return False
    return True

def get_invariant_factors(n, M):
    if n == 0:
        return []
    if len(M) == 0:
        return [0] * n
    
    mat = Matrix(M)
    rank = mat.rank()
    betti = n - rank
    
    factors = []
    prev_gcd = 1
    for k in range(1, rank + 1):
        gcd_k = 0
        for rows in combinations(M, k):
            subM_rows = [ [row[c] for c in range(n)] for row in rows ]
            for cols in combinations(range(n), k):
                subM = Matrix([ [r[c] for c in cols] for r in subM_rows ])
                det = int(abs(subM.det()))
                gcd_k = math.gcd(gcd_k, det)
                if gcd_k == 1:
                    break
            if gcd_k == 1:
                break
        if prev_gcd == 0:
            factors.append(0)
        else:
            factors.append(gcd_k // prev_gcd)
        prev_gcd = gcd_k
        
    factors = [f for f in factors if f > 1]
    return factors + [0] * betti

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        P1, P2 = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = is_valid_presentation(P1) and is_valid_presentation(P2)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            n1, rels1 = P1
            M1 = []
            for rel in rels1:
                row = [0] * n1
                for x in rel:
                    if x > 0:
                        row[x - 1] += 1
                    elif x < 0:
                        row[-x - 1] -= 1
                M1.append(row)
            inv1 = get_invariant_factors(n1, M1)
            
            n2, rels2 = P2
            M2 = []
            for rel in rels2:
                row = [0] * n2
                for x in rel:
                    if x > 0:
                        row[x - 1] += 1
                    elif x < 0:
                        row[-x - 1] -= 1
                M2.append(row)
            inv2 = get_invariant_factors(n2, M2)
            
            # If the abelianizations have different invariant factors, 
            # the groups are not isomorphic.
            # By Tietze's Equivalence Theorem, they cannot be transformed 
            # into each other by Tietze transformations.
            neg_q = bool(inv1 != inv2)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P_1 and P_2 are two finite group presentations",
    "¬Q: P_1 cannot be transformed into P_2 by a finite sequence of Tietze transformations"
]

N_HYP = 1
NEG_Q_INDEX = 1