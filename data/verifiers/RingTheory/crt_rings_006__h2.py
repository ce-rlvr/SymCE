import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools

# Top-level setup for potential witness expressions
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def parse_witness(witness):
    """
    Parses the witness into a standard format:
    (add_table, mul_table, I_indices, J_indices, m, n)
    """
    try:
        if isinstance(witness, dict):
            if 'add_t' in witness and 'mul_t' in witness:
                return witness['add_t'], witness['mul_t'], list(witness['I']), list(witness['J']), int(witness['m']), int(witness['n'])
            elif 'n_mod' in witness:
                size = int(witness['n_mod'])
                add_t = [[(i + j) % size for j in range(size)] for i in range(size)]
                mul_t = [[(i * j) % size for j in range(size)] for i in range(size)]
                return add_t, mul_t, list(witness['I']), list(witness['J']), int(witness['m']), int(witness['n'])
            
        if len(witness) == 5:
            R_obj, I_obj, J_obj, m, n = witness
            m, n = int(m), int(n)
            if isinstance(R_obj, int) or (hasattr(R_obj, 'is_Integer') and R_obj.is_Integer):
                size = int(R_obj)
                add_t = [[(i + j) % size for j in range(size)] for i in range(size)]
                mul_t = [[(i * j) % size for j in range(size)] for i in range(size)]
                I = list(I_obj)
                J = list(J_obj)
                return add_t, mul_t, I, J, m, n
            elif isinstance(R_obj, (list, tuple, set)):
                R_list = list(R_obj)
                elem_to_idx = {e: i for i, e in enumerate(R_list)}
                size = len(R_list)
                add_t = [[0] * size for _ in range(size)]
                mul_t = [[0] * size for _ in range(size)]
                for i, a in enumerate(R_list):
                    for j, b in enumerate(R_list):
                        add_t[i][j] = elem_to_idx[a + b]
                        mul_t[i][j] = elem_to_idx[a * b]
                I = [elem_to_idx[e] for e in I_obj]
                J = [elem_to_idx[e] for e in J_obj]
                return add_t, mul_t, I, J, m, n
        elif len(witness) == 6:
            add_t, mul_t, I, J, m, n = witness
            return list(add_t), list(mul_t), list(I), list(J), int(m), int(n)
    except Exception:
        pass
    return None

def is_comm_ring_with_id(add_t, mul_t):
    try:
        size = len(add_t)
        if size == 0: return False
        if len(mul_t) != size: return False
        for row in add_t + mul_t:
            if len(row) != size: return False
            for val in row:
                if not (0 <= val < size): return False
                
        # Commutativity
        for i in range(size):
            for j in range(size):
                if add_t[i][j] != add_t[j][i]: return False
                if mul_t[i][j] != mul_t[j][i]: return False
                
        # Associativity & Distributivity
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    if add_t[add_t[i][j]][k] != add_t[i][add_t[j][k]]: return False
                    if mul_t[mul_t[i][j]][k] != mul_t[i][mul_t[j][k]]: return False
                    if mul_t[i][add_t[j][k]] != add_t[mul_t[i][j]][mul_t[i][k]]: return False
                    
        # Additive identity
        zero = -1
        for i in range(size):
            if all(add_t[i][j] == j for j in range(size)):
                zero = i
                break
        if zero == -1: return False
        
        # Additive inverse
        for i in range(size):
            if not any(add_t[i][j] == zero for j in range(size)): return False
            
        # Multiplicative identity
        one = -1
        for i in range(size):
            if all(mul_t[i][j] == j for j in range(size)):
                one = i
                break
        if one == -1: return False
        
        return True
    except Exception:
        return False

def multiply_sets(A, B, mul_t):
    res = set()
    for a in A:
        for b in B:
            res.add(mul_t[a][b])
    return res

def get_products(A, m, mul_t):
    if not A:
        return set()
    res = None
    base = set(A)
    p = m
    while p > 0:
        if p % 2 == 1:
            if res is None:
                res = set(base)
            else:
                res = multiply_sets(res, base, mul_t)
        p //= 2
        if p > 0:
            base = multiply_sets(base, base, mul_t)
    return res

def additive_closure(S, add_t):
    if not S:
        return set()
    closure = set(S)
    queue = list(S)
    while queue:
        curr = queue.pop(0)
        for x in list(closure):
            nxt = add_t[curr][x]
            if nxt not in closure:
                closure.add(nxt)
                queue.append(nxt)
    return closure

def power_set(A, m, add_t, mul_t):
    if not A:
        return set()
    prods = get_products(A, m, mul_t)
    return additive_closure(prods, add_t)

def conditions(witness):
    parsed = parse_witness(witness)
    if parsed is None:
        return [False, False, False, False]
    
    add_t, mul_t, I, J, m, n = parsed
    
    # H_1: R is a commutative ring with identity
    h1 = is_comm_ring_with_id(add_t, mul_t)
    
    # H_2: I + J = R
    try:
        size = len(add_t)
        if not all(0 <= x < size for x in I):
            h2 = False
        elif not all(0 <= x < size for x in J):
            h2 = False
        else:
            sum_IJ = set()
            for i in I:
                for j in J:
                    sum_IJ.add(add_t[i][j])
            h2 = (len(sum_IJ) == size)
    except Exception:
        h2 = False
        
    # H_3: m and n are positive integers
    try:
        h3 = (m > 0) and (n > 0)
    except Exception:
        h3 = False
        
    # ¬Q: I^m + J^n != R
    try:
        Im = power_set(I, m, add_t, mul_t)
        Jn = power_set(J, n, add_t, mul_t)
        
        sum_Im_Jn = set()
        for i in Im:
            for j in Jn:
                sum_Im_Jn.add(add_t[i][j])
                
        neg_q = (len(sum_Im_Jn) != size)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I + J = R",
    "H_3: m and n are positive integers",
    "¬Q: I^m + J^n != R"
]

N_HYP = 3
NEG_Q_INDEX = 3