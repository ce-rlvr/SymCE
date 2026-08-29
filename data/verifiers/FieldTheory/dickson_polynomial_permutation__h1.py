import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (q, a, n) where:
      - q is the size of the ring/field F (the dropped hypothesis is that q is a prime power)
      - a is an element of F
      - n is the index of the Dickson polynomial
    """
    try:
        q, a, n = witness
        q = int(q)
        a = int(a)
        n = int(n)
    except Exception:
        return [False, False, False, False]
        
    try:
        # H1: a is a non-zero element of F
        h1 = (q >= 2 and a % q != 0)
    except Exception:
        h1 = False
        
    try:
        # H2: n is a positive integer
        h2 = (n >= 1)
    except Exception:
        h2 = False
        
    try:
        # H3: D_n(x, a) is the n-th Dickson polynomial of the first kind over F
        # This is a definitional hypothesis, so it holds by construction in our evaluation.
        h3 = True
    except Exception:
        h3 = False
        
    try:
        # Evaluate D_n(x, a) over Z_q using matrix exponentiation to ensure O(log n) time
        def mat_mult(A, B):
            return [
                [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % q, (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % q],
                [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % q, (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % q]
            ]

        def mat_pow(A, p):
            res = [[1, 0], [0, 1]]
            base = A
            while p > 0:
                if p % 2 == 1:
                    res = mat_mult(res, base)
                base = mat_mult(base, base)
                p //= 2
            return res

        def dickson(x):
            if n == 0:
                return 2 % q
            if n == 1:
                return x % q
            A = [[x % q, (-a) % q], [1, 0]]
            An = mat_pow(A, n - 1)
            return (An[0][0] * x + An[0][1] * 2) % q

        # Check if D_n(x, a) induces a permutation on F (Z_q)
        seen = set()
        is_pp = True
        for x in range(q):
            val = dickson(x)
            if val in seen:
                is_pp = False
                break
            seen.add(val)
            
        # The conclusion states: D_n(x, a) is a PP iff gcd(n, q^2 - 1) == 1
        gcd_cond = (math.gcd(n, q**2 - 1) == 1)
        
        # neg_Q is True if the conclusion FAILS (i.e., the iff statement is false)
        neg_q = (is_pp != gcd_cond)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a is a non-zero element of F",
    "H_2: n is a positive integer",
    "H_3: D_n(x, a) is the n-th Dickson polynomial of the first kind over F",
    "¬Q: D_n(x, a) induces a permutation on F if and only if gcd(n, q^2 - 1) = 1 fails"
]

N_HYP = 3
NEG_Q_INDEX = 3