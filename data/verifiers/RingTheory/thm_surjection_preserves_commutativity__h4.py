import itertools
import functools
import math
import sympy
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
# We define finite rings as tuples: (size, add_table, mul_table)
# Elements are integers 0, 1, ..., size - 1.

def MatrixRing(n, p):
    """Returns the ring of n x n matrices over Z_p."""
    elements = list(itertools.product(range(p), repeat=n*n))
    size = len(elements)
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    add_table = [[0]*size for _ in range(size)]
    mul_table = [[0]*size for _ in range(size)]
    
    for i, A in enumerate(elements):
        for j, B in enumerate(elements):
            # Addition
            C_add = tuple((a + b) % p for a, b in zip(A, B))
            add_table[i][j] = elem_to_idx[C_add]
            
            # Multiplication
            C_mul = [0] * (n * n)
            for r in range(n):
                for c in range(n):
                    val = sum(A[r*n + k] * B[k*n + c] for k in range(n)) % p
                    C_mul[r*n + c] = val
            mul_table[i][j] = elem_to_idx[tuple(C_mul)]
            
    return (size, add_table, mul_table)

def Z(n):
    """Returns the ring of integers modulo n."""
    add = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul = [[(i * j) % n for j in range(n)] for i in range(n)]
    return (n, add, mul)

def ProductRing(R1, R2):
    """Returns the direct product of two rings."""
    n1, add1, mul1 = R1
    n2, add2, mul2 = R2
    n = n1 * n2
    add = [[0]*n for _ in range(n)]
    mul = [[0]*n for _ in range(n)]
    for i in range(n1):
        for j in range(n2):
            idx1 = i * n2 + j
            for k in range(n1):
                for l in range(n2):
                    idx2 = k * n2 + l
                    add[idx1][idx2] = add1[i][k] * n2 + add2[j][l]
                    mul[idx1][idx2] = mul1[i][k] * n2 + mul2[j][l]
    return (n, add, mul)

# Common finite rings
M2_Z2 = MatrixRing(2, 2)
Z2 = Z(2)
Z3 = Z(3)
Z4 = Z(4)
Z6 = Z(6)

def is_ring(ring):
    """Helper to verify if a tuple represents a valid finite ring with identity."""
    try:
        n, add, mul = ring
        if not isinstance(n, int) or n <= 0: return False
        if not isinstance(add, list) or len(add) != n: return False
        if not isinstance(mul, list) or len(mul) != n: return False
        
        for row in add:
            if not isinstance(row, list) or len(row) != n: return False
        for row in mul:
            if not isinstance(row, list) or len(row) != n: return False
            
        # Check additive identity
        zero = None
        for i in range(n):
            if all(add[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None: return False

        # Check additive inverses
        for i in range(n):
            if not any(add[i][j] == zero for j in range(n)): return False

        # Check multiplicative identity
        one = None
        for i in range(n):
            if all(mul[i][j] == j and mul[j][i] == j for j in range(n)):
                one = i
                break
        if one is None: return False

        # Check commutativity of addition, associativity, and distributivity
        for i in range(n):
            for j in range(n):
                if add[i][j] != add[j][i]: return False
                for k in range(n):
                    if add[add[i][j]][k] != add[i][add[j][k]]: return False
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                    if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # H1: R and S are rings
    try:
        R, S, f = witness
        h1_ok = is_ring(R) and is_ring(S)
    except Exception:
        h1_ok = False

    # H2: f is a ring homomorphism
    try:
        R, S, f = witness
        n_R, add_R, mul_R = R
        n_S, add_S, mul_S = S
        
        h2_ok = True
        # Check well-definedness
        for i in range(n_R):
            try:
                val = f(i) if callable(f) else f[i]
                if not isinstance(val, int) or not (0 <= val < n_S):
                    h2_ok = False
                    break
            except Exception:
                h2_ok = False
                break
                
        if h2_ok:
            # Check homomorphism properties
            for i in range(n_R):
                for j in range(n_R):
                    fi = f(i) if callable(f) else f[i]
                    fj = f(j) if callable(f) else f[j]
                    f_add = f(add_R[i][j]) if callable(f) else f[add_R[i][j]]
                    f_mul = f(mul_R[i][j]) if callable(f) else f[mul_R[i][j]]
                    
                    if f_add != add_S[fi][fj]:
                        h2_ok = False
                        break
                    if f_mul != mul_S[fi][fj]:
                        h2_ok = False
                        break
                if not h2_ok:
                    break
            
        if h2_ok:
            # Check f(1_R) = 1_S
            def get_one(n, mul):
                for i in range(n):
                    if all(mul[i][j] == j and mul[j][i] == j for j in range(n)):
                        return i
                return None
            
            one_R = get_one(n_R, mul_R)
            one_S = get_one(n_S, mul_S)
            if one_R is not None and one_S is not None:
                f_one_R = f(one_R) if callable(f) else f[one_R]
                if f_one_R != one_S:
                    h2_ok = False
    except Exception:
        h2_ok = False

    # H3: f is surjective
    try:
        R, S, f = witness
        n_R = R[0]
        n_S = S[0]
        images = set()
        for i in range(n_R):
            val = f(i) if callable(f) else f[i]
            images.add(val)
        h3_ok = len(images) == n_S
    except Exception:
        h3_ok = False

    # neg_Q: S is not commutative
    try:
        R, S, f = witness
        n_S, add_S, mul_S = S
        neg_q_ok = False
        for i in range(n_S):
            for j in range(n_S):
                if mul_S[i][j] != mul_S[j][i]:
                    neg_q_ok = True
                    break
            if neg_q_ok:
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism",
    "H_3: f is surjective",
    "¬Q: S is not commutative"
]

N_HYP = 3
NEG_Q_INDEX = 3