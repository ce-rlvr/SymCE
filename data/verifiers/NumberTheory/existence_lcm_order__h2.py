import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import n_order
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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_order(x, n):
    if isinstance(x, (int, sympy.Integer)):
        x = int(x)
        if math.gcd(x, n) != 1:
            return None
        try:
            return n_order(x, n)
        except Exception:
            return None
            
    mat = None
    k = 0
    if hasattr(x, 'is_Matrix') and x.is_Matrix:
        if x.shape[0] != x.shape[1]:
            return None
        k = x.shape[0]
        for r in range(k):
            for c in range(k):
                if not x[r, c].is_integer:
                    return None
        mat = [[int(x[r, c]) % n for c in range(k)] for r in range(k)]
    elif isinstance(x, list) and all(isinstance(row, list) for row in x):
        k = len(x)
        if k == 0 or any(len(row) != k for row in x):
            return None
        for r in range(k):
            for c in range(k):
                if not isinstance(x[r][c], (int, sympy.Integer)):
                    return None
        mat = [[int(x[r][c]) % n for c in range(k)] for r in range(k)]
        
    if mat is not None:
        I = [[1 if r == c else 0 for c in range(k)] for r in range(k)]
        
        def mul(A, B):
            C = [[0]*k for _ in range(k)]
            for i in range(k):
                for j in range(k):
                    s = sum(A[i][m] * B[m][j] for m in range(k))
                    C[i][j] = s % n
            return C
            
        current = mat
        for i in range(1, 100001):
            if current == I:
                return i
            current = mul(current, mat)
        return None
        
    return None

def conditions(witness):
    try:
        n, a, b, h, k = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: n is an integer greater than 1
    try:
        h1 = isinstance(n, int) and n > 1
    except Exception:
        h1 = False
        
    # H2: The order of a modulo n is h
    try:
        order_a = get_order(a, n)
        h2 = (order_a is not None) and (order_a == h)
    except Exception:
        h2 = False
        
    # H3: The order of b modulo n is k
    try:
        order_b = get_order(b, n)
        h3 = (order_b is not None) and (order_b == k)
    except Exception:
        h3 = False
        
    # neg_Q: There does NOT exist an integer c coprime to n such that the order of c modulo n is exactly lcm(h, k)
    try:
        if not (isinstance(h, int) and isinstance(k, int)):
            neg_q = False
        else:
            target_order = math.lcm(h, k)
            try:
                max_order = sympy.ntheory.reduced_totient(n)
                neg_q = (max_order % target_order != 0)
            except Exception:
                # Fallback if reduced_totient is unavailable or fails
                neg_q = True
                for c in range(1, n):
                    if math.gcd(c, n) == 1:
                        try:
                            if n_order(c, n) == target_order:
                                neg_q = False
                                break
                        except Exception:
                            pass
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: The order of a modulo n is h",
    "H_3: The order of b modulo n is k",
    "¬Q: There does not exist an integer c coprime to n such that the order of c modulo n is exactly lcm(h, k)"
]

N_HYP = 3
NEG_Q_INDEX = 3