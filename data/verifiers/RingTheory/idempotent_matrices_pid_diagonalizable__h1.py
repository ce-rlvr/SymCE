import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import z3
import math
import itertools
import functools

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

def get_d_val(A_sympy):
    for atom in A_sympy.atoms(sympy.Pow):
        if atom.exp == sympy.Rational(1, 2):
            base = atom.base
            if base.is_Integer:
                if sympy.I in A_sympy.atoms():
                    return -int(base)
                return int(base)
    if sympy.I in A_sympy.atoms():
        return -1
    return 0

def extract_coeffs(expr, d_val):
    if d_val == 0:
        if expr.is_Integer:
            return int(expr), 0
        else:
            raise ValueError("Not an integer")
    if d_val == -1:
        sq = sympy.I
    elif d_val < 0:
        sq = sympy.sqrt(-d_val) * sympy.I
    else:
        sq = sympy.sqrt(d_val)
        
    expr = sympy.expand(expr)
    b = expr.coeff(sq)
    a = expr - b * sq
    if a.is_Integer and b.is_Integer:
        return int(a), int(b)
    else:
        raise ValueError("Not an integer")

def z3_det(matrix, d_val):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        a, b = matrix[0][0], matrix[0][1]
        c, d_m = matrix[1][0], matrix[1][1]
        
        def mul(x, y):
            return (x[0]*y[0] + d_val*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
        
        def sub(x, y):
            return (x[0]-y[0], x[1]-y[1])
            
        ad = mul(a, d_m)
        bc = mul(b, c)
        return sub(ad, bc)
        
    def mul(x, y):
        return (x[0]*y[0] + d_val*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
    def add(x, y):
        return (x[0]+y[0], x[1]+y[1])
    def sub(x, y):
        return (x[0]-y[0], x[1]-y[1])
        
    res = (0, 0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        cofactor = z3_det(submatrix, d_val)
        term = mul(matrix[0][j], cofactor)
        if j % 2 == 1:
            res = sub(res, term)
        else:
            res = add(res, term)
    return res

def check_diagonalizable_z3(A_sympy, d_val):
    n = A_sympy.shape[0]
    trace_val = sum(A_sympy[i, i] for i in range(n))
    trace_val = sympy.simplify(trace_val)
    
    if not trace_val.is_Integer:
        return True 
    trace = int(trace_val)
    if trace < 0 or trace > n:
        return True 
        
    D = [[1 if i == j and i < trace else 0 for j in range(n)] for i in range(n)]
    
    solver = z3.Solver()
    
    P_R = [[z3.Int(f"P_R_{i}_{j}") for j in range(n)] for i in range(n)]
    P_I = [[z3.Int(f"P_I_{i}_{j}") for j in range(n)] for i in range(n)]
    
    def mul(a, b):
        return (a[0]*b[0] + d_val*a[1]*b[1], a[0]*b[1] + a[1]*b[0])
        
    A_R = [[0]*n for _ in range(n)]
    A_I = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            a, b = extract_coeffs(A_sympy[i,j], d_val)
            A_R[i][j] = a
            A_I[i][j] = b
            
    for i in range(n):
        for j in range(n):
            ap_R, ap_I = 0, 0
            for k in range(n):
                a = (A_R[i][k], A_I[i][k])
                p = (P_R[k][j], P_I[k][j])
                prod = mul(a, p)
                ap_R = ap_R + prod[0]
                ap_I = ap_I + prod[1]
                
            pd_R = P_R[i][j] * D[j][j]
            pd_I = P_I[i][j] * D[j][j]
            
            solver.add(ap_R == pd_R, ap_I == pd_I)
            
    P_matrix = [[(P_R[i][j], P_I[i][j]) for j in range(n)] for i in range(n)]
    det_R, det_I = z3_det(P_matrix, d_val)
    
    norm = det_R*det_R - d_val*det_I*det_I
    solver.add(z3.Or(norm == 1, norm == -1))
    
    solver.set("timeout", 4000)
    res = solver.check()
    
    if res == z3.unsat:
        return True
    else:
        return False

def conditions(witness):
    # H_1: Let n be a positive integer (A is a square matrix)
    try:
        h1 = hasattr(witness, 'shape') and len(witness.shape) == 2 and witness.shape[0] == witness.shape[1] and witness.shape[0] > 0
    except Exception:
        h1 = False
        
    # H_2: Let A be an n x n matrix with entries in R
    try:
        if h1:
            d_val = get_d_val(witness)
            h2 = True
            for i in range(witness.shape[0]):
                for j in range(witness.shape[1]):
                    a, b = extract_coeffs(witness[i,j], d_val)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H_3: Assume A^2 = A
    try:
        if h1:
            diff = sympy.simplify(witness**2 - witness)
            h3 = diff == sympy.zeros(witness.shape[0], witness.shape[1])
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: A is not similar over R to a diagonal matrix whose diagonal entries are exclusively 1s and 0s
    try:
        if h1 and h2 and h3:
            d_val = get_d_val(witness)
            neg_q = check_diagonalizable_z3(witness, d_val)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer (A is a square matrix)",
    "H_2: A has entries in R",
    "H_3: A^2 = A",
    "¬Q: A is not similar over R to a diagonal matrix whose diagonal entries are exclusively 1s and 0s"
]

N_HYP = 3
NEG_Q_INDEX = 3