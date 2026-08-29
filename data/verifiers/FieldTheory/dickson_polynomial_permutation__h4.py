import sympy
from sympy import gcd
import itertools
from sympy.polys.galoistools import gf_irreducible_p, gf_add, gf_sub, gf_mul, gf_rem
from sympy.polys.domains import ZZ

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    "D_n(x, a) induces a permutation on F if and only if gcd(n, q^2 - 1) = 1"
    
    The witness should be a tuple: (q, a, n)
    where:
      - q is the order of the finite field (a prime power)
      - a is a non-zero element of F (represented as an integer or tuple of integers)
      - n is a positive integer
    """
    try:
        q, a, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a finite field of order q
    try:
        if not isinstance(q, (int, sympy.Integer)) or q < 2:
            h1 = False
            p, k = None, None
        else:
            q = int(q)
            factors = sympy.factorint(q)
            h1 = (len(factors) == 1)
            if h1:
                p = list(factors.keys())[0]
                k = factors[p]
            else:
                p, k = None, None
    except Exception:
        h1 = False

    # H_2: a is a non-zero element of F
    try:
        if not h1:
            h2 = False
        else:
            if k == 1:
                if isinstance(a, (int, sympy.Integer)):
                    h2 = (int(a) % p != 0)
                else:
                    h2 = False
            else:
                if isinstance(a, (tuple, list)):
                    h2 = any(int(c) % p != 0 for c in a)
                elif isinstance(a, (int, sympy.Integer)):
                    h2 = (int(a) % p != 0)
                else:
                    h2 = False
    except Exception:
        h2 = False

    # H_3: n is a positive integer
    try:
        h3 = isinstance(n, (int, sympy.Integer)) and int(n) > 0
    except Exception:
        h3 = False

    # neg_Q: The conclusion FAILS at the witness
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            n_val = int(n)
            gcd_val = gcd(n_val, q**2 - 1)
            expected_perm = (gcd_val == 1)

            if k == 1:
                a_val = int(a) % p
                def add_fn(u, v): return (u + v) % p
                def sub_fn(u, v): return (u - v) % p
                def mul_fn(u, v): return (u * v) % p
                zero = 0
                one = 1
                elements = list(range(p))
                
                def to_canonical(x): return x
            else:
                irred = None
                for coeffs in itertools.product(range(p), repeat=k):
                    poly = [1] + list(coeffs)
                    if gf_irreducible_p(poly, p, ZZ):
                        irred = poly
                        break
                if irred is None:
                    return [h1, h2, h3, False]
                
                if isinstance(a, (int, sympy.Integer)):
                    a_val = [int(a) % p]
                else:
                    a_val = [int(c) % p for c in a]
                
                while len(a_val) > 1 and a_val[0] == 0:
                    a_val.pop(0)
                if a_val == [0]:
                    a_val = []
                
                def add_fn(u, v): return gf_add(u, v, p, ZZ)
                def sub_fn(u, v): return gf_sub(u, v, p, ZZ)
                def mul_fn(u, v): return gf_rem(gf_mul(u, v, p, ZZ), irred, p, ZZ)
                zero = []
                one = [1]
                
                elements = []
                for coeffs in itertools.product(range(p), repeat=k):
                    val = list(coeffs)
                    while len(val) > 1 and val[0] == 0:
                        val.pop(0)
                    if not val: val = [0]
                    elements.append(val)
                
                def to_canonical(x):
                    res = list(x)
                    while len(res) > 1 and res[0] == 0:
                        res.pop(0)
                    if not res: res = [0]
                    return tuple(res)

            def mat_mul(A, B):
                return [
                    [add_fn(mul_fn(A[0][0], B[0][0]), mul_fn(A[0][1], B[1][0])),
                     add_fn(mul_fn(A[0][0], B[0][1]), mul_fn(A[0][1], B[1][1]))],
                    [add_fn(mul_fn(A[1][0], B[0][0]), mul_fn(A[1][1], B[1][0])),
                     add_fn(mul_fn(A[1][0], B[0][1]), mul_fn(A[1][1], B[1][1]))]
                ]
            
            def mat_pow(A, exp):
                res = [[one, zero], [zero, one]]
                base = A
                while exp > 0:
                    if exp % 2 == 1:
                        res = mat_mul(res, base)
                    base = mat_mul(base, base)
                    exp //= 2
                return res

            seen = set()
            is_perm = True
            for x_val in elements:
                if n_val == 0:
                    res = add_fn(one, one)
                elif n_val == 1:
                    res = x_val
                else:
                    M = [
                        [x_val, sub_fn(zero, a_val)],
                        [one, zero]
                    ]
                    M_pow = mat_pow(M, n_val - 1)
                    res = add_fn(mul_fn(M_pow[0][0], x_val), mul_fn(M_pow[0][1], add_fn(one, one)))
                
                canon = to_canonical(res)
                if canon in seen:
                    is_perm = False
                    break
                seen.add(canon)
            
            neg_q = (is_perm != expected_perm)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: a is a non-zero element of F",
    "H_3: n is a positive integer",
    "¬Q: D_n(x, a) induces a permutation on F iff gcd(n, q^2 - 1) = 1 is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3