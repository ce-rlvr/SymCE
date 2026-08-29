import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
import sympy.abc as abc
import itertools

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def contains(lst, item, eq):
    return any(eq(x, item) for x in lst)

def remove_duplicates(lst, eq):
    res = []
    for x in lst:
        if not contains(res, x, eq):
            res.append(x)
    return res

def is_subring(A, zero, add, mul, eq):
    if not A: return False
    if not contains(A, zero, eq): return False
    for a in A:
        for b in A:
            if not contains(A, add(a, b), eq): return False
            if not contains(A, mul(a, b), eq): return False
        has_inv = False
        for b in A:
            if eq(add(a, b), zero) and eq(add(b, a), zero):
                has_inv = True
                break
        if not has_inv: return False
    return True

def is_ideal(I, R, zero, add, mul, eq):
    for i in I:
        if not contains(R, i, eq): return False
    if not is_subring(I, zero, add, mul, eq): return False
    for i in I:
        for r in R:
            if not contains(I, mul(i, r), eq): return False
            if not contains(I, mul(r, i), eq): return False
    return True

def get_cosets(A, J, add, eq):
    cosets = []
    for a in A:
        coset_raw = [add(a, j) for j in J]
        coset = remove_duplicates(coset_raw, eq)
        is_new = True
        for c in cosets:
            if len(c) == len(coset) and all(contains(c, x, eq) for x in coset):
                is_new = False
                break
        if is_new:
            cosets.append(coset)
    return cosets

def quotient_ring_table(A, J, add, mul, eq):
    cosets = get_cosets(A, J, add, eq)
    k = len(cosets)
    add_table = [[-1]*k for _ in range(k)]
    mul_table = [[-1]*k for _ in range(k)]
    
    for i in range(k):
        a = cosets[i][0]
        for j in range(k):
            b = cosets[j][0]
            sum_ab = add(a, b)
            mul_ab = mul(a, b)
            
            sum_idx = -1
            for idx, c in enumerate(cosets):
                if contains(c, sum_ab, eq):
                    sum_idx = idx
                    break
            if sum_idx == -1: return None, None
            
            mul_idx = -1
            for idx, c in enumerate(cosets):
                if contains(c, mul_ab, eq):
                    mul_idx = idx
                    break
            if mul_idx == -1: return None, None
            
            add_table[i][j] = sum_idx
            mul_table[i][j] = mul_idx
            
    return add_table, mul_table

def are_isomorphic(add1, mul1, add2, mul2):
    if len(add1) != len(add2): return False
    k = len(add1)
    for p in itertools.permutations(range(k)):
        is_iso = True
        for i in range(k):
            for j in range(k):
                if p[add1[i][j]] != add2[p[i]][p[j]]:
                    is_iso = False
                    break
                if p[mul1[i][j]] != mul2[p[i]][p[j]]:
                    is_iso = False
                    break
            if not is_iso:
                break
        if is_iso:
            return True
    return False

def conclusion_holds(R, I, S, zero, add, mul, eq):
    S_cap_I = [x for x in S if contains(I, x, eq)]
    
    S_plus_I_raw = [add(s, i) for s in S for i in I]
    S_plus_I = remove_duplicates(S_plus_I_raw, eq)
    
    # 1. S \cap I is an ideal of S (implies S is a ring)
    if not is_subring(S, zero, add, mul, eq): return False
    if not is_ideal(S_cap_I, S, zero, add, mul, eq): return False
    
    # 2. S+I is a subring of R
    for x in S_plus_I:
        if not contains(R, x, eq): return False
    if not is_subring(S_plus_I, zero, add, mul, eq): return False
    
    # 3. (S+I)/I is isomorphic to S/(S \cap I)
    if not is_ideal(I, S_plus_I, zero, add, mul, eq): return False
    
    add1, mul1 = quotient_ring_table(S_plus_I, I, add, mul, eq)
    add2, mul2 = quotient_ring_table(S, S_cap_I, add, mul, eq)
    
    if add1 is None or add2 is None: return False
    
    return are_isomorphic(add1, mul1, add2, mul2)

def get_ops(witness):
    if isinstance(witness, tuple) and len(witness) == 4:
        try:
            n = int(witness[0])
            R, I, S = witness[1], witness[2], witness[3]
            def add(a, b): return (int(a) + int(b)) % n
            def mul(a, b): return (int(a) * int(b)) % n
            def eq(a, b): return (int(a) % n) == (int(b) % n)
            zero = 0
            return R, I, S, add, mul, eq, zero
        except Exception:
            pass
            
    if isinstance(witness, tuple) and len(witness) == 3:
        R, I, S = witness
        def add(a, b): return a + b
        def mul(a, b): return a * b
        def eq(a, b):
            try:
                if a == b: return True
            except:
                pass
            try:
                if hasattr(a, 'equals') and a.equals(b): return True
            except:
                pass
            try:
                diff = a - b
                if hasattr(diff, 'is_zero') and diff.is_zero: return True
            except:
                pass
            try:
                from sympy import simplify, MatrixBase
                if isinstance(diff, MatrixBase):
                    return diff.is_zero_matrix
                return simplify(diff) == 0
            except:
                return False
                
        zero = None
        for z in R:
            try:
                if all(eq(add(a, z), a) for a in R):
                    zero = z
                    break
            except:
                pass
        if zero is None: return None
        return R, I, S, add, mul, eq, zero
        
    return None

def conditions(witness) -> list[bool]:
    ops = get_ops(witness)
    if ops is None:
        return [False, False, False]
    R, I, S, add, mul, eq, zero = ops
    
    try:
        h1 = is_subring(R, zero, add, mul, eq)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ideal(I, R, zero, add, mul, eq)
    except Exception:
        h2 = False
        
    try:
        c_holds = conclusion_holds(R, I, S, zero, add, mul, eq)
        neg_q = not c_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "¬Q: S \\cap I is not an ideal of S, or S+I is not a subring of R, or (S+I)/I is not isomorphic to S/(S \\cap I)"
]

N_HYP = 2
NEG_Q_INDEX = 2