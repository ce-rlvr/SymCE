import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Top-level setup for potential witness expressions
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
    "H_1: P_n is the set of all n x n permutation matrices",
    "¬Q: P_n does not form a group under matrix multiplication isomorphic to S_n"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_permutation_matrix(M, n):
    if not hasattr(M, 'rows') or not hasattr(M, 'cols'):
        return False
    if M.rows != n or M.cols != n:
        return False
    for i in range(n):
        ones = 0
        zeros_count = 0
        for j in range(n):
            val = M[i,j]
            if val == 1: 
                ones += 1
            elif val == 0: 
                zeros_count += 1
            else: 
                return False
        if ones != 1 or zeros_count != n - 1:
            return False
    for j in range(n):
        ones = 0
        zeros_count = 0
        for i in range(n):
            val = M[i,j]
            if val == 1: 
                ones += 1
            elif val == 0: 
                zeros_count += 1
            else: 
                return False
        if ones != 1 or zeros_count != n - 1:
            return False
    return True

def conditions(witness):
    try:
        # Handle witness as an integer n
        if isinstance(witness, int):
            n = witness
            h1 = (n >= 0)
            q = (n > 0)
            return [h1, not q]
            
        # Handle witness as a tuple (n, P_n)
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
            n, P_n = witness
        else:
            # Handle witness as the set/list of matrices P_n
            P_n = witness
            if not isinstance(P_n, (list, set, tuple)):
                return [False, False]
            P_n = list(P_n)
            if len(P_n) == 0:
                return [False, False]
            n = P_n[0].rows

        h1 = True
        for M in P_n:
            if not is_permutation_matrix(M, n):
                h1 = False
                break
                
        if h1:
            unique = []
            for M in P_n:
                if not any(M == U for U in unique):
                    unique.append(M)
            if len(unique) != math.factorial(n):
                h1 = False
                
    except Exception:
        h1 = False

    try:
        if not h1:
            q = False
        else:
            # The group of n x n permutation matrices is isomorphic to S_n for n >= 1.
            # For n = 0, S_0 is undefined in standard formulations (e.g., SymPy's SymmetricGroup),
            # making it the counterexample to the dropped hypothesis (n >= 1).
            q = (n > 0)
    except Exception:
        q = False

    return [h1, not q]
