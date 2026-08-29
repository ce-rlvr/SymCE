import sympy
from sympy import symbols
import itertools
import math

# Top-level setup for potential witness expressions
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def parse_witness(witness):
    """
    Parses the witness into (n, add_table, mul_table, S).
    Supports:
      - (n, S) where n is an integer representing Z/nZ.
      - (n, add_table, mul_table, S) for an explicit finite ring.
      - (elements_list, add_table, mul_table, S) for an explicit finite ring with named elements.
    """
    if isinstance(witness, tuple):
        if len(witness) == 2:
            R_obj, S_obj = witness
            if isinstance(R_obj, int) and R_obj > 0:
                n = R_obj
                add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
                mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
                S = list(S_obj)
                return n, add_table, mul_table, S
        elif len(witness) == 4:
            obj1, add_table, mul_table, S_obj = witness
            if isinstance(obj1, int) and obj1 > 0:
                return obj1, add_table, mul_table, list(S_obj)
            elif isinstance(obj1, list):
                n = len(obj1)
                if isinstance(add_table[0][0], int) and 0 <= add_table[0][0] < n:
                    S = []
                    for s in S_obj:
                        if s in obj1:
                            S.append(obj1.index(s))
                        elif isinstance(s, int) and 0 <= s < n:
                            S.append(s)
                    return n, add_table, mul_table, S
                else:
                    elem_to_idx = {e: i for i, e in enumerate(obj1)}
                    add_t = [[elem_to_idx[add_table[i][j]] for j in range(n)] for i in range(n)]
                    mul_t = [[elem_to_idx[mul_table[i][j]] for j in range(n)] for i in range(n)]
                    S = [elem_to_idx[s] for s in S_obj]
                    return n, add_t, mul_t, S
    raise ValueError("Unrecognized witness format")

def is_commutative_ring(n, add_table, mul_table):
    if n <= 0: return False
    if len(add_table) != n or any(len(row) != n for row in add_table): return False
    if len(mul_table) != n or any(len(row) != n for row in mul_table): return False
    
    for i in range(n):
        for j in range(n):
            if not (0 <= add_table[i][j] < n): return False
            if not (0 <= mul_table[i][j] < n): return False

    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]: return False
            if mul_table[i][j] != mul_table[j][i]: return False

    for i in range(n):
        for j in range(n):
            ij_add = add_table[i][j]
            ij_mul = mul_table[i][j]
            for k in range(n):
                if add_table[ij_add][k] != add_table[i][add_table[j][k]]: return False
                if mul_table[ij_mul][k] != mul_table[i][mul_table[j][k]]: return False
                if mul_table[i][add_table[j][k]] != add_table[ij_mul][mul_table[i][k]]: return False

    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None: return False

    for i in range(n):
        if not any(add_table[i][j] == zero for j in range(n)): return False

    one = None
    for i in range(n):
        if all(mul_table[i][j] == j for j in range(n)):
            one = i
            break
    if one is None: return False

    return True

def is_mult_closed(n, mul_table, S):
    if not isinstance(S, (list, set, tuple)): return False
    S = set(S)
    if not S.issubset(range(n)): return False
    if len(S) == 0: return False
    
    for a in S:
        for b in S:
            if mul_table[a][b] not in S: return False
    return True

def is_not_reduced_localization(n, add_table, mul_table, S):
    S = set(S)
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
            
    for a in range(n):
        is_nilpotent = False
        a_k = a
        for k in range(1, n + 1):
            if any(mul_table[v][a_k] == zero for v in S):
                is_nilpotent = True
                break
            a_k = mul_table[a_k][a]
            
        if is_nilpotent:
            is_zero = any(mul_table[u][a] == zero for u in S)
            if not is_zero:
                return True
                
    return False

def conditions(witness) -> list[bool]:
    try:
        n, add_table, mul_table, S = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_commutative_ring(n, add_table, mul_table)
    except Exception:
        h1 = False
        
    try:
        h2 = is_mult_closed(n, mul_table, S)
    except Exception:
        h2 = False
        
    try:
        neg_q = is_not_reduced_localization(n, add_table, mul_table, S)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}R is not a reduced ring"
]

N_HYP = 2
NEG_Q_INDEX = 2