import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Matrix
import itertools

# Top-level setup for standard algebraic objects
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

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: (I+J)(I \\cap J) is not a subset of IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (m, R, I, J)
    where m is an integer modulus (use 0 for standard arithmetic over Z),
    and R, I, J are lists of matrices (either sympy.Matrix or lists of lists)
    representing the ring and its ideals.
    """
    try:
        m, R_raw, I_raw, J_raw = witness
        
        def standardize(matrices):
            std = set()
            for mat in matrices:
                if hasattr(mat, 'tolist'):
                    mat = mat.tolist()
                std.add(tuple(tuple(row) for row in mat))
            return std

        R = standardize(R_raw)
        I = standardize(I_raw)
        J = standardize(J_raw)
    except Exception:
        return [False, False, False]

    def mat_add(A, B):
        if m == 0:
            return tuple(tuple(x + y for x, y in zip(rowA, rowB)) for rowA, rowB in zip(A, B))
        return tuple(tuple((x + y) % m for x, y in zip(rowA, rowB)) for rowA, rowB in zip(A, B))

    def mat_neg(A):
        if m == 0:
            return tuple(tuple(-x for x in row) for row in A)
        return tuple(tuple((-x) % m for x in row) for row in A)

    def mat_mul(A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        cols_B = len(B[0])
        res = []
        for i in range(rows_A):
            row = []
            for j in range(cols_B):
                val = sum(A[i][k] * B[k][j] for k in range(cols_A))
                if m != 0:
                    val %= m
                row.append(val)
            res.append(tuple(row))
        return tuple(res)

    def is_ring(S):
        if not S: return False
        for a in S:
            for b in S:
                if mat_add(a, mat_neg(b)) not in S:
                    return False
                if mat_mul(a, b) not in S:
                    return False
        
        # Check for multiplicative identity (unital ring)
        has_id = False
        for e in S:
            is_id = True
            for a in S:
                if mat_mul(e, a) != a or mat_mul(a, e) != a:
                    is_id = False
                    break
            if is_id:
                has_id = True
                break
        if not has_id:
            return False
            
        return True

    def is_ideal(S, Ring):
        if not S: return False
        if not S.issubset(Ring): return False
        for a in S:
            for b in S:
                if mat_add(a, mat_neg(b)) not in S:
                    return False
        for r in Ring:
            for s in S:
                if mat_mul(r, s) not in S:
                    return False
                if mat_mul(s, r) not in S:
                    return False
        return True

    try:
        ring_ok = is_ring(R)
        h1 = ring_ok and is_ideal(I, R)
    except Exception:
        h1 = False

    try:
        ring_ok = is_ring(R)
        h2 = ring_ok and is_ideal(J, R)
    except Exception:
        h2 = False

    try:
        I_plus_J = set(mat_add(i, j) for i in I for j in J)
        I_cap_J = I.intersection(J)

        def product_ideal(A, B):
            if not A or not B:
                if R:
                    sample = next(iter(R))
                    zero = tuple(tuple(0 for _ in row) for row in sample)
                    return {zero}
                return set()
                
            generators = set(mat_mul(a, b) for a in A for b in B)
            closure = set(generators)
            queue = list(generators)
            max_size = len(R) if R else 1000
            
            while queue:
                if len(closure) > max_size:
                    break
                curr = queue.pop(0)
                for mat in list(closure):
                    nxt = mat_add(curr, mat)
                    if nxt not in closure:
                        closure.add(nxt)
                        queue.append(nxt)
            return closure

        LHS = product_ideal(I_plus_J, I_cap_J)
        RHS = product_ideal(I, J)

        neg_q = not LHS.issubset(RHS)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]