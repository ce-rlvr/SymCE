import sympy
from sympy import Matrix, eye, zeros, Symbol, simplify
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import functools
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_minpoly_degree(A):
    """
    Computes the degree of the minimal polynomial of a square matrix A.
    """
    if A.shape[0] == 0:
        return 0
        
    x = Symbol('x')
    charpoly = A.charpoly(x)
    factors = charpoly.factor_list()
    
    base_factors = [f[0] for f in factors[1]]
    max_mults = [f[1] for f in factors[1]]
    
    def poly_degree(mults):
        return sum(m * f.degree() for m, f in zip(mults, base_factors))
    
    ranges = [range(1, m + 1) for m in max_mults]
    mult_combinations = list(itertools.product(*ranges))
    mult_combinations.sort(key=poly_degree)
    
    n = A.shape[0]
    
    for mults in mult_combinations:
        pA = eye(n)
        for f, m in zip(base_factors, mults):
            coeffs = f.all_coeffs()
            fA = zeros(n, n)
            A_pow = eye(n)
            for c in reversed(coeffs):
                fA += c * A_pow
                A_pow = A_pow * A
            pA = pA * (fA**m)
            
        is_zero = True
        for i in range(n):
            for j in range(n):
                val = pA[i, j].expand()
                if val != 0:
                    if simplify(val) != 0:
                        is_zero = False
                        break
            if not is_zero:
                break
        if is_zero:
            return poly_degree(mults)
            
    return charpoly.degree()

def conditions(witness):
    A = None
    k = None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, k = witness
        else:
            A = witness
    except Exception:
        return [False, False, False]
        
    # H1: A is diagonalizable over F
    try:
        h1 = bool(A.is_diagonalizable())
    except Exception:
        h1 = False
        
    # H2: A has exactly k distinct eigenvalues
    try:
        eigenvals = A.eigenvals()
        if k is None:
            k = len(eigenvals)
        h2 = (len(eigenvals) == k)
    except Exception:
        h2 = False
        
    # ¬Q: The degree of the minimal polynomial of A is not exactly k
    try:
        if k is None:
            neg_q = False
        else:
            deg = get_minpoly_degree(A)
            neg_q = bool(deg != k)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is diagonalizable over F",
    "H_2: A has exactly k distinct eigenvalues",
    "¬Q: The degree of the minimal polynomial of A is not exactly k"
]

N_HYP = 2
NEG_Q_INDEX = 2