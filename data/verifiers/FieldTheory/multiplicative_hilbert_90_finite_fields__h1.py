import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools

# Top-level setup for potential witness references
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

def poly_mod(A, B, q):
    A = [a % q for a in A]
    B = [b % q for b in B]
    while len(A) >= len(B):
        if A[-1] == 0:
            A.pop()
            continue
        lead_A = A[-1]
        deg_diff = len(A) - len(B)
        for i in range(len(B)):
            A[i + deg_diff] = (A[i + deg_diff] - lead_A * B[i]) % q
        A.pop()
    while len(A) > 0 and A[-1] == 0:
        A.pop()
    return A

def poly_mul(A, B, mod_poly, q):
    if not A or not B:
        return []
    res = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            res[i+j] = (res[i+j] + a * b) % q
    return poly_mod(res, mod_poly, q)

def poly_pow(A, p, mod_poly, q):
    res = [1]
    base = A[:]
    while p > 0:
        if p % 2 == 1:
            res = poly_mul(res, base, mod_poly, q)
        base = poly_mul(base, base, mod_poly, q)
        p //= 2
    return res

def get_mult_matrix(alpha_poly, mod_poly, q):
    n = len(mod_poly) - 1
    matrix = []
    for i in range(n):
        poly = [0]*i + [1]
        prod = poly_mul(poly, alpha_poly, mod_poly, q)
        prod_pad = prod + [0]*(n - len(prod))
        matrix.append(prod_pad)
    return matrix

def is_invertible(poly, mod_poly, q):
    M = get_mult_matrix(poly, mod_poly, q)
    det = int(round(sp.Matrix(M).det())) % q
    return math.gcd(det, q) == 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
            mod_poly = witness.get('mod_poly')
            alpha = witness.get('alpha')
        elif isinstance(witness, tuple) and len(witness) == 4:
            q, n, mod_poly, alpha = witness
        else:
            q = getattr(witness, 'q', None)
            n = getattr(witness, 'n', None)
            mod_poly = getattr(witness, 'mod_poly', None)
            alpha = getattr(witness, 'alpha', None)
            
        h1 = False
        try:
            if isinstance(q, int) and q >= 2 and isinstance(n, int) and n >= 1:
                if isinstance(mod_poly, list) and len(mod_poly) == n + 1:
                    if mod_poly[-1] == 1:
                        h1 = True
        except Exception:
            pass
            
        h2 = False
        try:
            if h1 and (isinstance(alpha, list) or isinstance(alpha, int)):
                if isinstance(alpha, int):
                    alpha_list = [alpha]
                else:
                    alpha_list = alpha
                if len(alpha_list) == 0:
                    alpha_list = [0]
                alpha_mod = poly_mod(alpha_list, mod_poly, q)
                if is_invertible(alpha_mod, mod_poly, q):
                    h2 = True
        except Exception:
            pass
            
        neg_q_ok = False
        try:
            if h1 and h2:
                if q**n > 10000:
                    return [h1, h2, False]
                    
                if isinstance(alpha, int):
                    alpha_list = [alpha]
                else:
                    alpha_list = alpha
                if len(alpha_list) == 0:
                    alpha_list = [0]
                alpha_mod = poly_mod(alpha_list, mod_poly, q)
                
                M = get_mult_matrix(alpha_mod, mod_poly, q)
                det = int(round(sp.Matrix(M).det())) % q
                norm_is_one = (det == 1)
                
                exists_beta = False
                for coeffs in itertools.product(range(q), repeat=n):
                    beta = list(coeffs)
                    while len(beta) > 0 and beta[-1] == 0:
                        beta.pop()
                    if not beta:
                        continue
                    if is_invertible(beta, mod_poly, q):
                        beta_q = poly_pow(beta, q, mod_poly, q)
                        lhs = poly_mul(alpha_mod, beta_q, mod_poly, q)
                        if lhs == beta:
                            exists_beta = True
                            break
                
                if norm_is_one != exists_beta:
                    neg_q_ok = True
        except Exception:
            pass
            
        return [h1, h2, neg_q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: E = F_{q^n} is a finite extension of F_q",
    "H_2: alpha in E^x",
    "¬Q: N_{E/F_q}(alpha) = 1 iff exists beta in E^x such that alpha = beta / beta^q FAILS"
]

N_HYP = 2
NEG_Q_INDEX = 2